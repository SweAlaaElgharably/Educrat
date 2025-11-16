from django.db import models

# Create your models here.
class Category(models.Model):
    title_arabic = models.CharField(max_length=100)
    title_english = models.CharField(max_length=100)
    image = models.ImageField(upload_to="category")

class SubCategory(models.Model):
    title_arabic = models.CharField(max_length=100)
    title_english = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="sub_categories")