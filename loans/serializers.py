from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Loan

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'is_admin')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_admin=validated_data.get('is_admin', False)
        )
        return user

class OTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = '__all__'
        read_only_fields = ('user', 'monthly_installment', 'total_interest', 'total_amount', 'status', 'created_at', 'updated_at')

    def validate_amount(self, value):
        if value is None or value < 1000 or value > 100000:
            raise serializers.ValidationError("Loan amount must be between ₹1,000 and ₹100,000.")
        return value

    def validate_tenure(self, value):
        if value is None or value < 3 or value > 24:
            raise serializers.ValidationError("Loan tenure must be between 3 and 24 months.")
        return value

    def validate_interest_rate(self, value):
        if value is None or value < 0 or value > 100:
            raise serializers.ValidationError("Interest rate must be between 0% and 100%.")
        return value
