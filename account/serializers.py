from rest_framework import serializers
from account.models import AdminProfile, CustomerProfile, User, VendorProfile

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['email', 'name', 'phone', 'date_of_birth', 'password', 'password2', 'role']
        extra_kwargs = {
            'password': {'write_only': True},
        }
        
        # validate password and confirm password
    def validate(self, attrs):
        role = attrs.get('role')  
        if role == 'admin':
            raise serializers.ValidationError("Cannot create a user with role 'admin' using this API.")
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
        fields = ['email', 'password', 'role']
        
        
# Vendor Profile Serializer
class VendorProfileSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user.name', read_only=True)# Remove read only to make it writable
    email = serializers.EmailField(source='user.email', read_only=True)
    phone = serializers.CharField(source='user.phone', read_only=True)
    date_of_birth = serializers.DateField(source='user.date_of_birth', read_only=True)
    role = serializers.CharField(source='user.role', read_only=True)
    last_login = serializers.DateTimeField(source='user.last_login', read_only=True)
    is_active = serializers.BooleanField(source='user.is_active', read_only=True)
    created_at = serializers.DateTimeField(source='user.created_at', read_only=True)
    updated_at = serializers.DateTimeField(source='user.updated_at', read_only=True)
    class Meta:
        model = VendorProfile
        fields = ['user', 'profile_picture', 'business_type', 'business_name', 'address', 'name', 'email', 'phone', 'date_of_birth', 'role', 'last_login', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['user']  # 'user' will be set automatically based on the logged-in user


# Customer Profile Serializer
class CustomerProfileSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user.name', read_only=True)# Remove read only to make it writable
    email = serializers.EmailField(source='user.email', read_only=True)
    phone = serializers.CharField(source='user.phone', read_only=True)
    date_of_birth = serializers.DateField(source='user.date_of_birth', read_only=True)
    role = serializers.CharField(source='user.role', read_only=True)
    last_login = serializers.DateTimeField(source='user.last_login', read_only=True)
    is_active = serializers.BooleanField(source='user.is_active', read_only=True)
    created_at = serializers.DateTimeField(source='user.created_at', read_only=True)
    updated_at = serializers.DateTimeField(source='user.updated_at', read_only=True)
    
  
    class Meta:
        model = CustomerProfile
        fields = ['user', 'profile_picture', 'address', 'name', 'email', 'phone', 'date_of_birth', 'role', 'last_login', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['user']


# Admin Profile Serializer
class AdminProfileSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user.name', read_only=True)# Remove read only to make it writable
    email = serializers.EmailField(source='user.email', read_only=True)
    phone = serializers.CharField(source='user.phone', read_only=True)
    date_of_birth = serializers.DateField(source='user.date_of_birth', read_only=True)
    role = serializers.CharField(source='user.role', read_only=True)
    last_login = serializers.DateTimeField(source='user.last_login', read_only=True)
    is_active = serializers.BooleanField(source='user.is_active', read_only=True)
    created_at = serializers.DateTimeField(source='user.created_at', read_only=True)
    updated_at = serializers.DateTimeField(source='user.updated_at', read_only=True)
    
    
    class Meta:
        model = AdminProfile
        fields = ['user', 'profile_picture', 'permissions', 'name', 'email', 'phone', 'date_of_birth', 'role', 'last_login', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['user']