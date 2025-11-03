from .models import User
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer

class UserCreateSerializer(BaseUserCreateSerializer):
    re_password = serializers.CharField(write_only=True)
    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password', 're_password', 'phone', 'area_of_expertise', 'id_card_face', 'id_card_back']
    
    def validate(self, data):
        if data['password'] != data['re_password']:
            raise serializers.ValidationError({"re_password": "Passwords do not match."})
        return data



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone', 'bio', 'area_of_expertise', 'picture')








