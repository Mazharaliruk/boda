from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from account.serializers import UserLoginSerializer, UserRegistrationSerializer
from django.contrib.auth import authenticate

# Create your views here.

class UserRegistration(APIView):
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception= True):
            user = serializer.save()
            return Response(status=status.HTTP_200_OK, data={"message": "Registration successfully"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# user login view
class UserLogin(APIView):
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception= True):
            email = serializer.data.get("email")
            password = serializer.data.get("password")
            user = authenticate(email=email, password=password)
            if user is not None:
                return Response(status=status.HTTP_200_OK, data={"message": "Login successfully"})
            else:
                return Response(status=status.HTTP_404_NOT_FOUND, data={"message": "Invalid credentials email or password"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
