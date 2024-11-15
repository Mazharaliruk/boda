from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from account.models import(
    AdminProfile, 
    CustomerProfile, 
    VendorProfile)
from account.serializers import(
    AdminProfileSerializer,
    CustomerProfileSerializer,
    UserLoginSerializer,
    UserRegistrationSerializer, 
    VendorProfileSerializer
)
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.

# Genrate token menually 
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistration(APIView):
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception= True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response(status=status.HTTP_200_OK, data={"token":token,"message": "Registration successfully"})
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
                token = get_tokens_for_user(user)
                return Response(status=status.HTTP_200_OK, data={"token":token,"message": "Login successfully"})
            else:
                return Response(status=status.HTTP_404_NOT_FOUND, data={"message": "Invalid credentials email or password"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    


# User Profile View
class UserProfile(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        if user.role == 'vendor':
            profile = get_object_or_404(VendorProfile, user=user)
            serializer = VendorProfileSerializer(profile)
        elif user.role == 'customer':
            profile = get_object_or_404(CustomerProfile, user=user)
            serializer = CustomerProfileSerializer(profile)
        elif user.role == 'admin':
            profile = get_object_or_404(AdminProfile, user=user)
            serializer = AdminProfileSerializer(profile)
        else:
            return Response(
                {"message": "Invalid user role."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response(serializer.data, status=status.HTTP_200_OK)