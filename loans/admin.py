from django.contrib import admin
from .models import Loan, PaymentSchedule

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('loan_id', 'user', 'amount', 'tenure', 'interest_rate', 'status', 'created_at')
    search_fields = ('loan_id', 'user__email')
    list_filter = ('status', 'created_at')

@admin.register(PaymentSchedule)
class PaymentScheduleAdmin(admin.ModelAdmin):
    list_display = ('loan', 'installment_no', 'due_date', 'amount', 'status')
    search_fields = ('loan__loan_id',)
    list_filter = ('status', 'due_date')