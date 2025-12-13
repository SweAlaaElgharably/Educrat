from django.db import models
from user.models import User
from content.models import Content

# Create your models here.
class Lesson(models.Model):
    title = models.CharField(max_length=200)
    video = models.FileField(upload_to='lessons/videos/', blank=True, null=True)
    richtext = models.TextField(blank=True)
    pdf_file = models.FileField(upload_to='lessons/pdfs/', blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lessons')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='lessons')

    class Meta:
        unique_together = ('content', 'order')

    def __str__(self):
        return self.title