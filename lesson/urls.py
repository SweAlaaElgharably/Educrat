from django.urls import path
from .views import *

urlpatterns = [
    path('lesson/', LessonListView.as_view()),
    path('lesson/create', LessonCreateView.as_view()),
    path('lesson/<int:pk>', LessonRetrieveView.as_view()),
    path('lesson/<int:pk>/update', LessonUpdateView.as_view()),
    path('lesson/<int:pk>/delete', LessonDestroyView.as_view()),
]
