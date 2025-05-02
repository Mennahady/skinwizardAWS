from rest_framework.generics import CreateAPIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .serializers import (
    PatientRegisterSerializer,
    DoctorRegisterSerializer,
    PharmacyRegisterSerializer
)

# -----------------------------
# Patient Registration View
# -----------------------------
class PatientRegisterView(CreateAPIView):
    serializer_class = PatientRegisterSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]


# -----------------------------
# Doctor Registration View
# -----------------------------
class DoctorRegisterView(CreateAPIView):
    serializer_class = DoctorRegisterSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]


# -----------------------------
# Pharmacy Registration View
# -----------------------------
class PharmacyRegisterView(CreateAPIView):
    serializer_class = PharmacyRegisterSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]



