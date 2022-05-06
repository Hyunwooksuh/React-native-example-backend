from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializers import UserSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.contrib import auth
import jwt

# Create your views here.
class RegisterView (GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        serilizer=UserSerializer(data=request.data)

        if serilizer.is_valid():
            serilizer.save()
            return Response(serilizer.data, status=status.HTTP_201_CREATED)
        
        return Response(serilizer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(GenericAPIView):
    serializer_class=LoginSerializer

    def post(self, request):
        data=request.data
        username=data.get('username', '')
        password=data.get('password', '')
        user=auth.authenticate(username=username, password=password)

        if user:
            auth_token=jwt.encode({'username': user.username}, settings.JWT_SECRET_KEY, algorithm="HS256")
        
            serilizer=UserSerializer(user)

            data={
                'user': serilizer.data,
                'token': auth_token,
            }

            return Response(data, status=status.HTTP_200_OK)


        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

