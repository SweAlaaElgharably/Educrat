from django.db import models
from user.models import User
from content.models import Content

# Create your models here.
class Order(models.Model):
    STATUS = (("pending", "Pending"), ("paid", "Paid"), ("failed", "Failed"),)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    tap_charge_id = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=20)

class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)