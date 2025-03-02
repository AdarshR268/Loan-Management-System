from django.urls import path
from .views import RegisterView, VerifyOTPView, LoginView, ProfileView, LogoutView, RefreshTokenView

urlpatterns = [
    path('', RegisterView.as_view(), name='register'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('refresh-token/', RefreshTokenView.as_view(), name='refresh-token'),
]