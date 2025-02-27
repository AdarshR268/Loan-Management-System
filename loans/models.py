from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username, email, password, **extra_fields)

# Custom User Model
class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_admin = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, null=True, blank=True)

    groups = models.ManyToManyField(
        Group,
        related_name="loans_users",  # 🔹 Fix: Avoids clash with `auth.User.groups`
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="loans_user_permissions",  # 🔹 Fix: Avoids clash with `auth.User.user_permissions`
        blank=True
    )

    objects = UserManager()

    def __str__(self):
        return self.username

# Loan Model
class Loan(models.Model):
    LOAN_STATUS_CHOICES = [
        ("ACTIVE", "Active"),
        ("CLOSED", "Closed"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="loans")
    amount = models.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(1000), MaxValueValidator(100000)]
    )
    tenure = models.IntegerField(
        validators=[MinValueValidator(3), MaxValueValidator(24)]
    )
    interest_rate = models.DecimalField(
        max_digits=5, decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    monthly_installment = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_interest = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=LOAN_STATUS_CHOICES, default="ACTIVE")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Loan {self.id} - {self.user.username}"
