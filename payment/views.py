import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os
from content.models import Content
from .models import *
from .serializers import OrderSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from user.permissions import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from content.models import Content
from content.serializers import ContentSerializer

# Create your views here.

TAP_SECRET = os.environ.get("TAP_SECRET")     

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_charge(request):
    data = request.data
    method = data.get("method", "src_all")
    phone = ""
    if method == "card":
        method = "src_card"
    elif method == "mada":
        method = "src_sa.mada"
    elif method == "apple":
        method = "src_apple_pay"
    elif method == "samsung":
        method = "src_samsung_pay"
    elif method == "stcpay":
        method = "src_sa.stcpay"
        phone = data.get("phone", "")
    order = Order.objects.create(user=request.user, amount=data["amount"], status="pending", method=method)
    payload = {
        "amount": data.get("amount"),
        "currency": "SAR",
        "customer": {
            "first_name": data.get("first_name"),
            "last_name": data.get("last_name"),
            "email": data.get("email"),
        },
        "merchant": {"id": "68015154"},
        "source": {"id": method},
        "metadata": {"order_id": order.id, "courses": data.get("courses")},
        "post": {"url": "https://api.cr-ai.cloud/webhook/"},
        "redirect": {"url": "https://www.cr-ai.cloud/en/payment/success"}
    }
    if phone:
        payload["source"]["phone"] = {"country_code": "966", "number": phone}
    res = requests.post("https://api.tap.company/v2/charges", json=payload, headers={"Authorization": f"Bearer {TAP_SECRET}", "Content-Type": "application/json",})
    response = res.json()
    print("TAP RESPONSE:", response)  
    if res.status_code != 200:
        order.delete()
        return JsonResponse({"error": response}, status=400)
    charge_id = response.get("id")
    url = response.get("transaction", {}).get("url") or None
    return JsonResponse({"url": url, "id": charge_id, "order_id": order.id}) 

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_charge(request):
    data = request.data
    charge_id = data.get("id")
    otp = data.get("otp")
    if not charge_id or not otp:
        return JsonResponse({"error": "id and otp are required"}, status=400)
    payload = {
        "gateway_response": {
            "name": "STC_PAY",
            "response": {
                "reference": {
                    "otp": otp
                }
            }
        }
    }
    res = requests.put(f"https://api.tap.company/v2/charges/{charge_id}", json=payload, headers={"Authorization": f"Bearer {TAP_SECRET}", "Content-Type": "application/json",})
    response = res.json()
    print("TAP UPDATE RESPONSE:", response)
    if res.status_code != 200:
        return JsonResponse({"error": response}, status=400)
    return JsonResponse(response)
    
@api_view(["POST"])
@permission_classes([AllowAny])
def tap_webhook(request):
    try:
        payload = request.data
    except Exception:
        return JsonResponse({"ok": False}, status=200)
    status = payload.get("status")
    charge_id = payload.get("id")
    metadata = payload.get("metadata", {})
    order_id = metadata.get("order_id")
    course_ids = metadata.get("courses", [])
    print("WEBHOOK PAYLOAD:", payload)
    if not order_id:
        return JsonResponse({"ok": False, "error": "No order_id"}, status=200)
    try:
        order = Order.objects.get(id=int(order_id))
    except Order.DoesNotExist:
        return JsonResponse({"ok": False, "error": "Order not found"}, status=200)
    except (ValueError, TypeError):
        return JsonResponse({"ok": False, "error": "Invalid order_id"}, status=200)
    if status == "CAPTURED":
        order.status = "paid"
        order.tap_charge_id = charge_id
        order.save()
        for cid in course_ids:
            try:
                Enrollment.objects.get_or_create(user=order.user, content=int(cid))
            except Exception as e:
                print(f"Enrollment error for course {cid}: {e}")
    elif status == "FAILED":
        order.status = "failed"
        order.save()
    return JsonResponse({"ok": True}, status=200)

# The CRUD Operations of Orders and Enrollments
class OrderListView(ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]
    
class OrderRetrieveView(RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]
        
# User Content
class MyContentAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ContentSerializer
    def get_queryset(self):
        return Content.objects.filter(enrollment__user=self.request.user).select_related("subcategory", "creator")