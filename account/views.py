from tokenize import TokenError
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from account.models import(
    AdminProfile, 
    CustomerProfile,
    User, 
    VendorProfile)
from account.permissions import IsAdmin
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
    
    
    
class UserLogin(APIView):
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get("email")
            password = serializer.data.get("password")
            role = serializer.data.get("role")

            # Authenticate user
            user = authenticate(email=email, password=password)
            if user is not None:
                # Check if the user's role matches the provided role
                if hasattr(user, "role") and user.role == role:
                    token = get_tokens_for_user(user)
                    return Response(
                        status=status.HTTP_200_OK,
                        data={"token": token, "message": "Login successfully"}
                    )
                else:
                    return Response(
                        status=status.HTTP_403_FORBIDDEN,
                        data={"message": "Invalid role for this user"}
                    )
            else:
                return Response(
                    status=status.HTTP_404_NOT_FOUND,
                    data={"message": "Invalid credentials: email or password"}
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
    
class UserLogout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        try:
            refresh_token = request.data.get("refresh_token")
            if not refresh_token:
                return Response({"message": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

            # Blacklist the refresh token
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
        except TokenError as e:
            return Response({"message": "Invalid or expired token", "error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"message": "Logout failed", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UserProfile(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        profile = None
        serializer = None
        print(user)
        print(user.role)
        # Check role and retrieve profile
        if user.role == 'vendor':
            try:
                profile = get_object_or_404(VendorProfile, user=user)
                serializer = VendorProfileSerializer(profile)
            except VendorProfile.DoesNotExist:
                return Response(
                    {"message": "Vendor profile not found."},
                    status=status.HTTP_404_NOT_FOUND
                )
        elif user.role == 'customer':
            try:
                profile = get_object_or_404(CustomerProfile, user=user)
                serializer = CustomerProfileSerializer(profile)
            except CustomerProfile.DoesNotExist:
                return Response(
                    {"message": "Customer profile not found."},
                    status=status.HTTP_404_NOT_FOUND
                )
        elif user.role == 'admin':
            print("Admin profile found.")
            try:
                profile = get_object_or_404(AdminProfile, user=user)
                serializer = AdminProfileSerializer(profile)
            except AdminProfile.DoesNotExist:
                return Response(
                    {"message": "Admin profile not found."},
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {"message": "Invalid user role."},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
# fetch all users 
class UserList(APIView):
    permission_classes = [IsAdmin]

    def get(self, request, format=None):
        customers = CustomerProfile.objects.filter(user__role='customer')
        serializer = CustomerProfileSerializer(customers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    

# fetch customer by id
class CustomerById(APIView):
    permission_classes = [IsAdmin]

    # Fetch customer by ID
    def get(self, request, pk, format=None):
        customer = get_object_or_404(CustomerProfile, pk=pk)
        serializer = CustomerProfileSerializer(customer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Update customer by ID
    # Update customer by ID
    def put(self, request, pk, format=None):
        customer = get_object_or_404(CustomerProfile, pk=pk)
        serializer = CustomerProfileSerializer(customer, data=request.data, partial=True)
        
        if serializer.is_valid():
            validated_data = serializer.validated_data

            # Update CustomerProfile fields
            customer.profile_picture = validated_data.get('profile_picture', customer.profile_picture)
            customer.address = validated_data.get('address', customer.address)
            customer.save()

            # Update related User fields
            user_data = validated_data.get('user', {})
            user = customer.user
            user.name = user_data.get('name', user.name)
            # user.email = user_data.get('email', user.email)
            # user.phone = user_data.get('phone', user.phone)
            # user.date_of_birth = user_data.get('date_of_birth', user.date_of_birth)
            user.save()

            return Response(
                {"message": "Customer updated successfully", "data": serializer.data},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete customer by ID
    def delete(self, request, pk, format=None):
        customer = get_object_or_404(CustomerProfile, pk=pk)
        customer.delete()
        return Response({"message": "Customer deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


#fetch all vendors
class VendorList(APIView):
    permission_classes = [IsAdmin]

    def get(self, request, format=None):
        vendors = VendorProfile.objects.filter(user__role='vendor')
        serializer = VendorProfileSerializer(vendors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)