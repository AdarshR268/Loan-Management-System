from django.urls import path
from .views import LoanView, ForecloseLoanView, AdminLoanView

urlpatterns = [
    path('', LoanView.as_view(), name='loans'),
    path('<str:loan_id>/foreclose/', ForecloseLoanView.as_view(), name='foreclose-loan'),
    path('admin/', AdminLoanView.as_view(), name='admin-loan-view'),
]