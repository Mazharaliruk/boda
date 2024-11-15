from rest_framework import serializers
from account.models import AdminProfile, CustomerProfile, User, VendorProfile

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['email', 'name', 'phone', 'date_of_birth', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True},
        }
        
        # validate password and confirm password
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password and confirm password does not match")
        return attrs
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
    
    
    # User Login Serializer
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['email', 'password']
        
        
# Vendor Profile Serializer
class VendorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorProfile
        fields = ['user', 'profile_picture', 'business_type', 'business_name', 'address']
        read_only_fields = ['user']  # 'user' will be set automatically based on the logged-in user


# Customer Profile Serializer
class CustomerProfileSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user.name', read_only=True)# Remove read only to make it writable
    email = serializers.EmailField(source='user.email', read_only=True)
    phone = serializers.CharField(source='user.phone', read_only=True)
    date_of_birth = serializers.DateField(source='user.date_of_birth', read_only=True)
    
  
    class Meta:
        model = CustomerProfile
        fields = ['user', 'profile_picture', 'address', 'name', 'email', 'phone', 'date_of_birth']
        read_only_fields = ['user']


# Admin Profile Serializer
class AdminProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminProfile
        fields = ['user', 'profile_picture', 'permissions']
        read_only_fields = ['user']