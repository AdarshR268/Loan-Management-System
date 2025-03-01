from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated  
from rest_framework_simplejwt.tokens import RefreshToken  
from .models import User
import random
import requests
from django.core.mail import send_mail
from .serializers import RefreshTokenSerializer

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        role = request.data.get('role', 'USER')  

        # Validate role
        if role not in ['ADMIN', 'USER']:
            return Response({"error": "Invalid role. Choose 'ADMIN' or 'USER'."}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({"error": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(email=email, password=password, role=role)

        # Generate and send OTP
        otp = random.randint(1000, 9999)
        user.otp = str(otp)  # Save the OTP to the user model
        user.save()


        # Call the deployed Node.js email service to send OTP
        try:
            response = requests.post(
                'https://otp-email-service-g7i9.onrender.com/send-otp',  # Updated Render service URL
                json={'email': email, 'otp': otp},  # Send email and OTP to Node.js
                headers={'Content-Type': 'application/json'}  # Set content type to JSON
            )

            # Check if the OTP email was sent successfully
            if response.status_code == 200:
                return Response({"message": "OTP sent to your email"}, status=status.HTTP_201_CREATED)
            else:
                # Handle failure to send OTP email
                return Response({"error": "Failed to send OTP email"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            # Handle exceptions (e.g., Node.js server is down)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')
        user = User.objects.filter(email=email).first()

        if user and user.otp == otp:  # Check the OTP
            user.is_verified = True
            user.otp = None  # Clear the OTP after verification
            user.save()
            return Response({"message": "User verified successfully"}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = User.objects.filter(email=email).first()

        # Check if the user exists and the password is correct
        if user and user.check_password(password):
            if not user.is_verified:
                return Response(
                    {"error": "User is not verified. Please verify your OTP first."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Invalid credentials."},
                status=status.HTTP_401_UNAUTHORIZED
            )

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]  # Requires authentication

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()  # Blacklist the refresh token
            return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]  # Requires authentication

    def get(self, request):
        user = request.user
        return Response({
            "id": user.id,
            "email": user.email,
            "role": user.role,
            "is_verified": user.is_verified,
        }, status=status.HTTP_200_OK)
    
class RefreshTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RefreshTokenSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        refresh_token = serializer.validated_data['refresh_token']

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            return Response({
                "access": access_token,
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": "Invalid or expired refresh token."},
                status=status.HTTP_400_BAD_REQUEST
            )