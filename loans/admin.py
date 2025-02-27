from django.contrib import admin
from .models import User, Loan

# Register User and Loan models in the admin panel
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_admin', 'is_verified')
    search_fields = ('username', 'email')
    list_filter = ('is_admin', 'is_verified')

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'amount', 'tenure', 'interest_rate', 'status')
    search_fields = ('user__username', 'id')
    list_filter = ('status',)
