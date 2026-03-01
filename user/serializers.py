from .models import User
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer

class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password', 'phone', 'area_of_expertise', 'id_card_face', 'id_card_back']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone', 'bio', 'area_of_expertise', 'picture', 'username', 'id_card_face', 'id_card_back')

class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'phone', 'bio', 'area_of_expertise', 'picture', 'is_influencer', 'is_verified', 'username', 'id_card_face', 'id_card_back')







