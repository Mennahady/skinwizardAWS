"""
URL configuration for skinwizard project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
#from rest_framework.documentation import include_docs_urls
#from rest_framework.schemas import get_schema_view

""" API Documentation
schema_view = get_schema_view(
    title="SkinWizard API",
    description="API endpoints for SkinWizard application",
    version="1.0.0"
)
"""
# API URL patterns
api_patterns = [
    # Authentication endpoints
    path('auth/', include([
        path('', include('dj_rest_auth.urls')),  # login, logout, password reset only
        path('social/', include('allauth.socialaccount.urls')),  # social auth
    ])),
# Custom registration for doctors and patients 
    path('accounts/', include('accounts.urls')),  
    # Application endpoints
    path('pharmacy/', include('pharmacy.urls')),
    path('diagnosis/', include('diagnosis.urls')),
    path('patient/', include('patient_form.urls')),
    path('consultation/', include('consultation.urls')),
    path('content/', include('content.urls')),
# API Documentation
    #path('docs/', include_docs_urls(title='SkinWizard API Documentation')),
    #path('schema/', schema_view),
]

urlpatterns = [
    # Admin interface
    path('admin/', admin.site.urls),

    # API endpoints (all under /api/)
    path('api/', include(api_patterns)),

    # OAuth2 Social Authentication Callbacks
    path('accounts/', include('allauth.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

