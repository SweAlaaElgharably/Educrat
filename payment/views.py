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

# Create your views here.

TAP_SECRET = os.environ.get("TAP_SECRET")

@csrf_exempt
def create_charge(request):
    if request.method == "POST":
        data = json.loads(request.body)
        method = data.get("method", "src_all")
        if method == "card":
            method = "src_card"
        elif method == "mada":
            method = "src_sa.mada"
        elif method == "apple":
            method = "src_apple_pay"
        elif method == "samsung":
            method = "src_samsung_pay"
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
            "metadata": {"order_id": 1, "courses": data.get("courses")},
            "post": {"url": "#"},
            "redirect": {"url": "#"}
        }
        res = requests.post("https://api.tap.company/v2/charges", json=payload, headers={"Authorization": f"Bearer {TAP_SECRET}", "Content-Type": "application/json",},);
        response = res.json()
        url = response.get("transaction", {}).get("url")
        return JsonResponse({"url": transaction_url})

@csrf_exempt
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
        
# # User Courses
# from .models import Course, Enrollment
# from .serializers import CourseSerializer

# class MyCoursesAPIView(ListAPIView):
#     serializer_class = CourseSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return Course.objects.filter(
#             enrollment__user=self.request.user
#         ).distinct()