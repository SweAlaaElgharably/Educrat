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
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from content.models import Content
from content.serializers import ContentSerializer

# Create your views here.

TAP_SECRET = os.environ.get("TAP_SECRET")

{
    "amount": 10,
    "currency": "SAR",
    "metadata": {"order_id": "test 1", "courses": "test 2"},
    "customer":{"first_name":"test", "last_name":"test", "email":"test@test.com"},
    "merchant": {"id": "68015154"},   
    "source": {"id": "src_sa.stcpay", "phone": {"country_code": "966", "number": "548220713"}},
    "post": {"url": "https://api.cr-ai.cloud/webhook/"},
    "redirect": {"url": "https://www.cr-ai.cloud/en/payment/success"}
}




@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_charge(request):
    if request.method == "POST":
        data = json.loads(request.body)
        method = data.get("method", "src_all")
        phone = ""
        if method == "card": method = "src_card"
        elif method == "mada": method = "src_sa.mada"
        elif method == "apple": method = "src_apple_pay"
        elif method == "samsung": method = "src_samsung_pay"
        elif method == "stcpay": 
            method = "src_sa.stcpay"
            try:
                phone = data.get("phone")
            except:
                phone = ""
        order = Order.objects.create(user = request.user, amount = data["amount"], status = "pending", method = method)
        payload = {
            "amount": data.get("amount"),
            "currency": "SAR",
            "customer": {
                "first_name": data.get("first_name"),
                "last_name": data.get("last_name"),
                "email": data.get("email"),
            },
            "merchant": {"id": "68023551"},
            "source": {"id": method},
            "metadata": {"order_id": order.id, "courses": data.get("courses")},
            "post": {"url": "https://api.cr-ai.cloud/webhook/"},
            "redirect": {"url": "https://www.cr-ai.cloud/en/payment/success"}
        }
        if phone:
            payload["source"]["phone"] = {"country_code": "966", "number": phone}
        res = requests.post("https://api.tap.company/v2/charges", json=payload, headers={"Authorization": f"Bearer {TAP_SECRET}", "Content-Type": "application/json",},);
        response = res.json()
        url = response.get("transaction", {}).get("url")
        id = response.get("id")
        return JsonResponse({"url": url, "id": id})

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def update_charge(request):
    if request.method == "POST":
        data = json.loads(request.body)
        id = data.get("id")
        otp = data.get("otp")
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
        res = requests.put(f"https://api.tap.company/v2/charges/{id}", json=payload, headers={"Authorization": f"Bearer {TAP_SECRET}", "Content-Type": "application/json",},);
        response = res.json()
        return JsonResponse(response)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def tap_webhook(request):
    payload = json.loads(request.body)
    status = payload.get("status")
    charge_id = payload.get("id")
    order_id = payload.get("metadata", {}).get("order_id")
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return JsonResponse({"error": "Order not found"})
    if status == "CAPTURED":
        order.status = "paid"
        order.tap_charge_id = charge_id
        order.save()
        course_ids = payload.get("metadata", {}).get("courses", [])
        for cid in course_ids:
            Enrollment.objects.get_or_create(user=order.user, course_id=cid)
    elif status == "FAILED":
        order.status = "failed"
        order.save()
    return JsonResponse({"ok": True})

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