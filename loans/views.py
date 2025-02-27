from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from .models import Loan, User
from .serializers import LoanSerializer, UserRegistrationSerializer, OTPSerializer
import random

# Permission class to check if the user is an admin
class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_admin

# User Registration View
class UserRegistrationView(APIView):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Generate OTP
            otp = random.randint(100000, 999999)
            user.otp = otp
            user.save()
            # Send OTP via email
            send_mail(
                'OTP for Email Verification',
                f'Your OTP is: {otp}',
                'noreply@loanmanagement.com',
                [user.email],
                fail_silently=False,
            )
            return Response({'message': 'OTP sent to your email.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# OTP Verification View
class OTPVerificationView(APIView):
    def get(self, request):
        return render(request, 'verify_otp.html')

    def post(self, request):
        serializer = OTPSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']
            user = User.objects.filter(email=email).first()
            if user and user.otp == otp:
                user.is_verified = True
                user.save()
                return Response({'message': 'Email verified successfully.'}, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Login View
class LoginView(APIView):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate the user
        user = authenticate(username=username, password=password)
        if not user:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        # Generate JWT token
        refresh = RefreshToken.for_user(user)

        # Include the user's role in the token payload
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        return Response({
            'access_token': access_token,
            'refresh_token': refresh_token,
            'role': 'admin' if user.is_admin else 'user'
        }, status=status.HTTP_200_OK)

# Loan Create View
class LoanCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return render(request, 'create_loan.html')

    def post(self, request):
        serializer = LoanSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Loan List View
class LoanListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        loans = Loan.objects.filter(user=request.user)
        serializer = LoanSerializer(loans, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Loan Detail View
class LoanDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, loan_id):
        loan = get_object_or_404(Loan, id=loan_id, user=request.user)
        serializer = LoanSerializer(loan)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Loan Foreclosure View
class LoanForeclosureView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, loan_id):
        loan = get_object_or_404(Loan, id=loan_id, user=request.user)
        if loan.status == 'ACTIVE':
            loan.status = 'CLOSED'
            loan.save()
            return Response({'message': 'Loan foreclosed successfully.'}, status=status.HTTP_200_OK)
        return Response({'error': 'Loan is already closed.'}, status=status.HTTP_400_BAD_REQUEST)

# Admin Dashboard View
class AdminDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        loans = Loan.objects.all()
        serializer = LoanSerializer(loans, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Admin User Management View
class AdminUserManagementView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        users = User.objects.all()
        serializer = UserRegistrationSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Profile View
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'username': user.username,
            'email': user.email,
            'is_admin': user.is_admin,
        }, status=status.HTTP_200_OK)

# About Us View
class AboutUsView(APIView):
    def get(self, request):
        return render(request, 'about_us.html')

# Contact Us View
class ContactUsView(APIView):
    def get(self, request):
        return render(request, 'contact_us.html')

# Forgot Password View
class ForgotPasswordView(APIView):
    def get(self, request):
        return render(request, 'forgot_password.html')

    def post(self, request):
        email = request.data.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            # Generate OTP
            otp = random.randint(100000, 999999)
            user.otp = otp
            user.save()
            # Send OTP via email
            send_mail(
                'OTP for Password Reset',
                f'Your OTP is: {otp}',
                'noreply@loanmanagement.com',
                [user.email],
                fail_silently=False,
            )
            return Response({'message': 'OTP sent to your email.'}, status=status.HTTP_200_OK)
        return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)