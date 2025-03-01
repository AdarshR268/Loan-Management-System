
from django.contrib import admin
from django.urls import path,include
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to the Loan Management System!")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),

     # API endpoints
    path('api/users/', include('users.urls')),
    path('api/loans/', include('loans.urls')),
]
