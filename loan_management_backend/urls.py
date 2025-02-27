from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin panel
    path('api/', include('loans.urls')),  # Include loans app URLs
    path('accounts/', include('allauth.urls')),  # Include allauth URLs
]

# Serve static files during development
from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
