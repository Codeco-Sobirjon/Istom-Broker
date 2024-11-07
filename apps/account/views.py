# yourapp/views.py
from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from .serializers import UserSignupSerializer, UserSigninSerializer
from .models import CustomUser


class UserSignupView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=UserSignupSerializer)
    def post(self, request, *args, **kwargs):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User created successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserSigninView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=UserSigninSerializer)
    def post(self, request, *args, **kwargs):
        serializer = UserSigninSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoleListView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(responses={200: "List of all available roles"})
    def get(self, request, *args, **kwargs):
        roles = Group.objects.values_list('name', flat=True)
        return Response({"roles": roles}, status=status.HTTP_200_OK)
