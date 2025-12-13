from django.db import models
from user.models import User
from category.models import SubCategory

# Create your models here.
class Content(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name="contents")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contents")
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
    