from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    DoctorRegistrationView,
    PatientRegistrationView,
    PharmacyRegisterView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
)

urlpatterns = [
    # Specialized registration endpoints
    path('register/doctor/', DoctorRegistrationView.as_view(), name='doctor_register'),
    path('register/patient/', PatientRegistrationView.as_view(), name='patient_register'),
    path('register/pharmacy/', PharmacyRegisterView.as_view(), name='pharmacy_register'),
    
    # Login endpoint
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Password reset endpoints
    path('password/reset/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password/reset/confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
] 