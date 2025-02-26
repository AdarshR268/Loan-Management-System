import os
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file
load_dotenv()

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',  # Django REST Framework
    'rest_framework_simplejwt',  # JWT Authentication
    # 'rest_framework_authtoken',
    'corsheaders',  # CORS Headers for cross-origin requests
    'loans',  # Loans app
    'allauth',  # Django Allauth for social authentication
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',  # Google OAuth
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # CORS Middleware
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware', 
]

ROOT_URLCONF = 'loan_management_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # Template directory
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',  # Required for allauth
            ],
        },
    },
]

WSGI_APPLICATION = 'loan_management_backend.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DATABASE_NAME'),
        'USER': os.getenv('DATABASE_USER'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD'),
        'HOST': os.getenv('DATABASE_HOST', 'localhost'),
        'PORT': os.getenv('DATABASE_PORT', '5432'),
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)

STATIC_URL = 'static/'
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'static'),  # Static files directory
# ]

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework and JWT Configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # JWT Authentication
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',  # Require authentication for all endpoints
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),  # Access token lifetime
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),  # Refresh token lifetime
}

# CORS Configuration (allow all origins for development)
CORS_ALLOW_ALL_ORIGINS = True

# Custom User Model
AUTH_USER_MODEL = 'loans.User'

# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('GAPPMAIL')  # Email address for sending emails
EMAIL_HOST_PASSWORD = os.getenv('GAPSWD')  # Email password
DEFAULT_FROM_EMAIL = 'LoanManagementSystem <loanmanagementsystem@gmail.com>'  # Default sender email
CONTACT_EMAIL = os.getenv('GAPPMAIL')  # Contact email

# Authentication Backends
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # Default Django authentication
    'allauth.account.auth_backends.AuthenticationBackend',  # Allauth for social authentication
]

# Allauth Configuration
SITE_ID = 1  # Required for allauth
LOGIN_REDIRECT_URL = 'home'  # Redirect after login
LOGOUT_REDIRECT_URL = 'login_admin'  # Redirect after logout

# Social Authentication (Google OAuth)
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'OAUTH_PKCE_ENABLED': True,
        'APP': {
            'client_id': os.getenv('GCLIENT_ID'),  # Google OAuth client ID
            'secret': os.getenv('GSECRET'),  # Google OAuth secret
            'key': ''
        }
    }
}

#========== RAZORPAY INTEGRATIONS =========#


RAZORPAY_KEY_ID = os.getenv('RAZORPAY_ID')
RAZORPAY_SECRET_KEY = os.getenv('RAZORPAY_SECRETKEY')
