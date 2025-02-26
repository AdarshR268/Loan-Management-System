from django.urls import path
from .views import (
    UserRegistrationView, OTPVerificationView, LoginView,
    LoanCreateView, LoanListView, LoanDetailView, LoanForeclosureView,
    AdminDashboardView,
)

urlpatterns = [
    
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('verify-otp/', OTPVerificationView.as_view(), name='verify-otp'),
    path('login/', LoginView.as_view(), name='login'),
    path('loans/create/', LoanCreateView.as_view(), name='create-loan'),
    path('loans/', LoanListView.as_view(), name='loan-list'),
    path('loans/<int:loan_id>/', LoanDetailView.as_view(), name='loan-detail'),
    path('loans/<int:loan_id>/foreclose/', LoanForeclosureView.as_view(), name='foreclose-loan'),
    path('admin-dashboard/', AdminDashboardView.as_view(), name='admin-dashboard'),
]