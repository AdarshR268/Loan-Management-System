from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from loans.models import User, Loan

class LoanTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword123')
        self.client.force_authenticate(user=self.user)
        self.create_loan_url = reverse('create-loan')
        self.valid_loan_payload = {
            'amount': 10000,
            'tenure': 12,
            'interest_rate': 10,
        }

    def test_loan_creation(self):
        response = self.client.post(self.create_loan_url, self.valid_loan_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Loan.objects.count(), 1)
        self.assertEqual(Loan.objects.get().amount, 10000)

    def test_loan_foreclosure(self):
        loan = Loan.objects.create(user=self.user, amount=10000, tenure=12, interest_rate=10)
        foreclosure_url = reverse('loan-foreclosure', args=[loan.id])
        response = self.client.post(foreclosure_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Loan.objects.get().status, 'CLOSED')
