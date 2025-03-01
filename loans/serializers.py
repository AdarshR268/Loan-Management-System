from rest_framework import serializers
from .models import Loan, PaymentSchedule

class PaymentScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentSchedule
        fields = ['installment_no', 'due_date', 'amount', 'status']

class LoanSerializer(serializers.ModelSerializer):
    payment_schedules = PaymentScheduleSerializer(many=True, read_only=True)

    class Meta:
        model = Loan
        fields = [
            'loan_id', 'amount', 'tenure', 'interest_rate', 'monthly_installment',
            'total_interest', 'total_amount', 'amount_paid', 'amount_remaining',
            'status', 'created_at', 'payment_schedules'
        ]