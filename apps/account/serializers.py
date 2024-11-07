# yourapp/serializers.py
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group
from rest_framework import serializers
from .models import CustomUser


class UserSignupSerializer(serializers.ModelSerializer):
    role = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'email', 'address', 'phone', 'avatar', 'role')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        role_name = validated_data.pop('role', None)
        user = CustomUser.objects.create_user(**validated_data)
        if role_name:
            try:
                role_group = Group.objects.get(name=role_name)
                user.groups.add(role_group)
            except Group.DoesNotExist:
                raise serializers.ValidationError({"role": "Role does not exist."})
        return user


class UserSigninSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid credentials")
