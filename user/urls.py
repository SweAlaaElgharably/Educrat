from django.urls import path,include
from .views import *

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('auth/adminuserlist/', AdminUserListView.as_view()),
    path('auth/adminuserlist/<int:pk>', AdminUserRetrieveView.as_view()),
    path('auth/adminuserlist/<int:pk>/update', AdminUserUpdateView.as_view()),
    path('auth/adminuserlist/<int:pk>/delete', AdminUserDestroyView.as_view()),
]
