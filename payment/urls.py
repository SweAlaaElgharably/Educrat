from django.urls import path
from .views import *

urlpatterns = [
    path("create-charge/", create_charge),
    path('order/', OrderListView.as_view()),
    path('order/<int:pk>', OrderRetrieveView.as_view()),
    path('my-content/', MyContentAPIView.as_view()),
]
