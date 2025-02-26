from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

# Custom User Model
class User(AbstractUser):
    is_admin = models.BooleanField(default=False)  # Role: Admin or User
    is_verified = models.BooleanField(default=False)  # Email verification status
    otp = models.CharField(max_length=6, null=True, blank=True)  # OTP for email verification

    def __str__(self):
        return self.username

# Loan Model
class Loan(models.Model):
    LOAN_STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('CLOSED', 'Closed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loans')  # User who created the loan
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(1000), MaxValueValidator(100000)]  # Loan amount validation
    )
    tenure = models.IntegerField(
        validators=[MinValueValidator(3), MaxValueValidator(24)]  # Tenure validation (3 to 24 months)
    )
    interest_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)]  # Interest rate validation (0% to 100%)
    )
    monthly_installment = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Monthly installment
    total_interest = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Total interest
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Total amount payable
    status = models.CharField(max_length=20, choices=LOAN_STATUS_CHOICES, default='ACTIVE')  # Loan status
    created_at = models.DateTimeField(auto_now_add=True)  # Loan creation date
    updated_at = models.DateTimeField(auto_now=True)  # Loan last updated date

    def calculate_monthly_installment(self):
        # Calculate monthly installment using compound interest formula
        monthly_interest_rate = (self.interest_rate / 100) / 12
        numerator = self.amount * monthly_interest_rate * (1 + monthly_interest_rate) ** self.tenure
        denominator = (1 + monthly_interest_rate) ** self.tenure - 1
        self.monthly_installment = numerator / denominator
        self.total_interest = self.monthly_installment * self.tenure - self.amount
        self.total_amount = self.amount + self.total_interest

    def save(self, *args, **kwargs):
        # Calculate monthly installment before saving
        self.calculate_monthly_installment()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Loan {self.id} - {self.user.username}"