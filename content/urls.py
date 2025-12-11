from django.urls import path
from .views import *

urlpatterns = [
    path('content/', ContentListView.as_view()),
    path('content/create', ContentCreateView.as_view()),
    path('content/<int:pk>', ContentRetrieveView.as_view()),
    path('content/<int:pk>/update', ContentUpdateView.as_view()),
    path('content/<int:pk>/delete', ContentDestroyView.as_view()),
]
