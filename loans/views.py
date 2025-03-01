from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsAdmin, IsUser
from .models import Loan, PaymentSchedule
from .serializers import LoanSerializer
from datetime import datetime, timedelta
from decimal import Decimal
from users.models import User
from django.db import transaction

# function to validate loan input
def validate_loan_input(amount, tenure, interest_rate):
    """
    Validate loan input data (amount, tenure, interest_rate).
    Returns a tuple (is_valid, error_response).
    """
    if not amount or not tenure or not interest_rate:
        return False, {
            "status": "error",
            "message": "All fields (amount, tenure, interest_rate) are required.",
            "data": None
        }

    try:
        amount = float(amount)
        if amount < 1000 or amount > 100000:
            return False, {
                "status": "error",
                "message": "Loan amount must be between ₹1,000 and ₹100,000",
                "data": None
            }
    except (ValueError, TypeError):
        return False, {
            "status": "error",
            "message": "Invalid amount. Amount must be a valid number.",
            "data": None
        }

    try:
        tenure = int(tenure)
        if tenure < 3 or tenure > 24:
            return False, {
                "status": "error",
                "message": "Loan tenure must be between 3 and 24 months",
                "data": None
            }
    except (ValueError, TypeError):
        return False, {
            "status": "error",
            "message": "Invalid tenure. Tenure must be a valid integer.",
            "data": None
        }

    try:
        interest_rate = float(interest_rate)
        if interest_rate < 1 or interest_rate > 30:
            return False, {
                "status": "error",
                "message": "Interest rate must be between 1% and 30%.",
                "data": None
            }
    except (ValueError, TypeError):
        return False, {
            "status": "error",
            "message": "Invalid interest rate. Interest rate must be a valid number.",
            "data": None
        }

    return True, None

class LoanView(APIView):
    permission_classes = [IsAuthenticated, IsUser]

    def post(self, request):
        """
        Handle POST requests to add a new loan.
        """
        amount = request.data.get('amount')
        tenure = request.data.get('tenure')
        interest_rate = request.data.get('interest_rate')

        # Validate input data
        is_valid, error_response = validate_loan_input(amount, tenure, interest_rate)
        if not is_valid:
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

        # Generate a unique loan_id using a thread-safe counter
        try:
            with transaction.atomic():
                # Get the latest loan_id and increment it atomically
                latest_loan = Loan.objects.select_for_update().order_by('-loan_id').first()
                if latest_loan:
                    latest_id = int(latest_loan.loan_id.replace("LOAN", ""))
                    new_id = latest_id + 1
                else:
                    new_id = 1
                loan_id = f"LOAN{new_id}"
        except Exception as e:
            return Response(
                {
                    "status": "error",
                    "message": "Failed to generate loan ID.",
                    "data": None
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Calculate monthly installment and total interest
        monthly_interest_rate = (interest_rate / 100) / 12
        monthly_installment = (amount * monthly_interest_rate) / (1 - (1 + monthly_interest_rate) ** (-tenure))
        total_interest = (monthly_installment * tenure) - amount
        total_amount = amount + total_interest

        # Create the loan
        loan = Loan.objects.create(
            user=request.user,
            loan_id=loan_id,  
            amount=amount,
            tenure=tenure,
            interest_rate=interest_rate,
            monthly_installment=monthly_installment,
            total_interest=total_interest,
            total_amount=total_amount,
            amount_remaining=total_amount,
        )

        # Create payment schedule
        today = datetime.now()
        for i in range(1, tenure + 1):
            due_date = today + timedelta(days=30 * i)
            PaymentSchedule.objects.create(
                loan=loan,
                installment_no=i,
                due_date=due_date,
                amount=monthly_installment,
            )

        serializer = LoanSerializer(loan)
        return Response({
            "status": "success",
            "message": "Loan created successfully.",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)

    def get(self, request):
        
        user = request.user
        status_filter = request.query_params.get('status', None)
        loans = Loan.objects.filter(user=user)  # Only fetch loans for the logged-in user
        if status_filter:
            loans = loans.filter(status=status_filter)
        serializer = LoanSerializer(loans, many=True)
        return Response({
            "status": "success",
            "message": "Loans retrieved successfully.",
            "data": {"loans": serializer.data}
        }, status=status.HTTP_200_OK)

class ForecloseLoanView(APIView):
    permission_classes = [IsAuthenticated, IsUser]

    def post(self, request, loan_id):
        """
        Handle POST requests to foreclose a loan.
        """
        # Get loan_id from the request body
        body_loan_id = request.data.get('loan_id')

        
        if loan_id != body_loan_id:
            return Response(
                {
                    "status": "error",
                    "message": "Loan ID in the URL does not match the Loan ID in the request body.",
                    "data": None
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Fetch the loan from the database
        try:
            loan = Loan.objects.get(loan_id=loan_id, user=request.user)  
        except Loan.DoesNotExist:
            return Response(
                {
                    "status": "error",
                    "message": "Loan not found or you do not have permission to access this loan.",
                    "data": None
                },
                status=status.HTTP_404_NOT_FOUND
            )

        # Check if the loan is active
        if loan.status != 'ACTIVE':
            return Response(
                {
                    "status": "error",
                    "message": "Loan is not active.",
                    "data": None
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Calculate foreclosure discount and final settlement amount
        foreclosure_discount = loan.total_interest * Decimal('0.1')  # 10% discount on interest
        final_settlement_amount = loan.total_amount - foreclosure_discount

        # Update loan status and amount paid
        loan.amount_paid = final_settlement_amount
        loan.amount_remaining = Decimal('0')  # Set amount_remaining to 0
        loan.status = 'FORECLOSED'
        loan.save()

        return Response({
            "status": "success",
            "message": "Loan foreclosed successfully.",
            "data": {
                "loan_id": loan.loan_id,
                "amount_paid": final_settlement_amount,
                "foreclosure_discount": foreclosure_discount,
                "final_settlement_amount": final_settlement_amount,
                "status": loan.status,
            }
        }, status=status.HTTP_200_OK)

class AdminLoanView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]  # Only admin can access this view

    def get(self, request):
        
        loans = Loan.objects.all()
        loan_data = []
        for loan in loans:
            loan_data.append({
                "loan_id": loan.loan_id,
                "user_id": loan.user.id,
                "user_email": loan.user.email,
                "amount": loan.amount,
                "tenure": loan.tenure,
                "interest_rate": loan.interest_rate,
                "monthly_installment": loan.monthly_installment,
                "total_interest": loan.total_interest,
                "total_amount": loan.total_amount,
                "amount_paid": loan.amount_paid,
                "amount_remaining": loan.amount_remaining,
                "status": loan.status,
                "created_at": loan.created_at,
            })

        return Response(
            {"status": "success", "message": "Loans retrieved successfully.", "data": loan_data},
            status=status.HTTP_200_OK
        )

    def post(self, request):
        """
        Handle POST requests to list loans for a specific user (admin only).
        """
        user_id = request.data.get('user_id')
        if not user_id:
            return Response(
                {"status": "error", "message": "user_id is required in the request body.", "data": None},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if the user exists
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"status": "error", "message": f"User with ID {user_id} does not exist.", "data": None},
                status=status.HTTP_404_NOT_FOUND
            )

        # Fetch loans for the given user_id
        loans = Loan.objects.filter(user_id=user_id)

        # Check if any loans exist for the user
        if not loans.exists():
            return Response(
                {
                    "status": "success",
                    "message": f"User {user.email} (ID: {user_id}) has not taken any loans.",
                    "data": None
                },
                status=status.HTTP_200_OK
            )

        # Serialize and return the loans
        serializer = LoanSerializer(loans, many=True)
        return Response(
            {
                "status": "success",
                "message": f"Loans for user {user.email} (ID: {user_id}):",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

    def delete(self, request):
        """
        Handle DELETE requests to delete a specific loan (admin only).
        """
        loan_id = request.data.get('loan_id')
        if not loan_id:
            return Response(
                {"status": "error", "message": "loan_id is required in the request body.", "data": None},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Fetch the loan by loan_id
        loan = Loan.objects.filter(loan_id=loan_id).first()
        if not loan:
            return Response(
                {"status": "error", "message": f"Loan with ID {loan_id} not found.", "data": None},
                status=status.HTTP_404_NOT_FOUND
            )

        user = loan.user

        deleted_loan_details = {
            "user_id": user.id,
            "user_email": user.email,
            "loan_id": loan.loan_id,
        }

        # Delete the loan
        loan.delete()
        return Response(
            {"status": "success", "message": "Loan deleted successfully.", "data": deleted_loan_details},
            status=status.HTTP_200_OK
        )