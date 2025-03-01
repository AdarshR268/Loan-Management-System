from django.db import models
from users.models import User

class Loan(models.Model):
    LOAN_STATUS = [
        ('ACTIVE', 'Active'),
        ('CLOSED', 'Closed'),
        ('FORECLOSED', 'Foreclosed'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loans')
    loan_id = models.CharField(max_length=20, unique=True, editable=False)  
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    tenure = models.IntegerField()
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    monthly_installment = models.DecimalField(max_digits=10, decimal_places=2)
    total_interest = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    amount_remaining = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=LOAN_STATUS, default='ACTIVE', db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.loan_id

class PaymentSchedule(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='payment_schedules')
    installment_no = models.IntegerField()
    due_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=[('PAID', 'Paid'), ('UNPAID', 'Unpaid')], default='UNPAID')

    def __str__(self):
        return f"Installment {self.installment_no} for Loan {self.loan.loan_id}"