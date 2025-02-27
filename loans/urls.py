from django.urls import path
from .views import (
    UserRegistrationView, OTPVerificationView, LoginView,
    LoanCreateView, LoanListView, LoanDetailView, LoanForeclosureView,
    AdminDashboardView, ProfileView, AdminUserManagementView,
    AboutUsView, ContactUsView, ForgotPasswordView,
)

urlpatterns = [
    # Authentication
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('verify-otp/', OTPVerificationView.as_view(), name='verify-otp'),
    path('login/', LoginView.as_view(), name='login'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),

    # Loan Management
    path('loans/create/', LoanCreateView.as_view(), name='create-loan'),
    path('loans/', LoanListView.as_view(), name='loan-list'),
    path('loans/<int:loan_id>/', LoanDetailView.as_view(), name='loan-detail'),
    path('loans/<int:loan_id>/foreclose/', LoanForeclosureView.as_view(), name='foreclose-loan'),

    # Admin
    path('admin-dashboard/', AdminDashboardView.as_view(), name='admin-dashboard'),
    path('admin/users/', AdminUserManagementView.as_view(), name='admin-user-management'),

    # Profile
    path('profile/', ProfileView.as_view(), name='profile'),

    # Optional Pages
    path('about-us/', AboutUsView.as_view(), name='about-us'),
    path('contact-us/', ContactUsView.as_view(), name='contact-us'),
]