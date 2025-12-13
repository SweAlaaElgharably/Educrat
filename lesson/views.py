from .models import Lesson
from .serializers import LessonSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, CreateAPIView
from rest_framework.permissions import AllowAny
from user.permissions import *
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

# Create your views here.
class LessonListView(ListAPIView):
    queryset = Lesson
    serializer_class = LessonSerializer
    permission_classes = [AllowAny]
    
class LessonCreateView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsVerifiedAndInfluencer]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

class LessonRetrieveView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [AllowAny]
    
class LessonUpdateView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsOwnerOrAdmin]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

class LessonDestroyView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsOwnerOrAdmin]
