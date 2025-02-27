from django.db.models.signals import post_save
from django.dispatch import receiver
from loans.models import Loan

@receiver(post_save, sender=Loan)
def send_loan_confirmation_email(sender, instance, created, **kwargs):
    """
    Send a confirmation email when a new loan is created.
    """
    if created:
        # You may replace this print statement with actual email sending logic
        print(f"Loan {instance.id} created. Sending confirmation email to {instance.user.email}.")
