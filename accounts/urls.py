from django.urls import path
from .views import (
    DoctorRegistrationView,
    PatientRegistrationView,
    PharmacyRegisterView,
)

urlpatterns = [
    # Specialized registration endpoints
    path('register/doctor/', DoctorRegistrationView.as_view(), name='doctor_register'),
    path('register/patient/', PatientRegistrationView.as_view(), name='patient_register'),
    path('register/pharmacy/', PharmacyRegisterView.as_view(), name='pharmacy_register'),
] 