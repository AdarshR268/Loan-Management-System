from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Loan

User = get_user_model()

# User Registration Serializer
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Password field (write-only)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'is_admin')  # Fields for user registration

    def create(self, validated_data):
        # Create a new user
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_admin=validated_data.get('is_admin', False)
        )
        return user

# OTP Verification Serializer
class OTPSerializer(serializers.Serializer):
    email = serializers.EmailField()  # Email field for OTP verification
    otp = serializers.CharField(max_length=6)  # OTP field

# Loan Serializer
class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = '__all__'  # Include all fields in the serializer
        read_only_fields = ('user', 'monthly_installment', 'total_interest', 'total_amount', 'status', 'created_at', 'updated_at')  # Read-only fields

    def validate_amount(self, value):
        # Validate loan amount
        if value < 1000 or value > 100000:
            raise serializers.ValidationError("Loan amount must be between ₹1,000 and ₹100,000.")
        return value

    def validate_tenure(self, value):
        # Validate loan tenure
        if value < 3 or value > 24:
            raise serializers.ValidationError("Loan tenure must be between 3 and 24 months.")
        return value

    def validate_interest_rate(self, value):
        # Validate interest rate
        if value < 0 or value > 100:
            raise serializers.ValidationError("Interest rate must be between 0% and 100%.")
        return value