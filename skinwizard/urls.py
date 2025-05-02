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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
    path('api/accounts/', include('accounts.urls')),  # your custom endpoints
    path('accounts/', include('allauth.urls')),  # for OAuth callbacks
    path('api/pharmacy/', include('pharmacy.urls')),
    path('api/diagnosis/', include('diagnosis.urls')),
    path('api/patient_form/', include('patient_form.urls')),
    path('api/consultation/', include('consultation.urls')),
    path('api/content/', include('content.urls')),


    # Social login
    path('auth/social/', include('allauth.socialaccount.urls')),
  
  

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

