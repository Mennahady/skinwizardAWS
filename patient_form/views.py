from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from .models import PatientForm, Doctor, ChatMessage, Patient
from .serializers import PatientFormSerializer, DoctorSerializer, ChatMessageSerializer
from rest_framework.response import Response
from rest_framework import status

class PatientFormViewSet(viewsets.ModelViewSet):
    queryset = PatientForm.objects.all()
    serializer_class = PatientFormSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Create or get patient instance for the current user
        patient, created = Patient.objects.get_or_create(
            user=self.request.user,
            defaults={'name': f"{self.request.user.first_name} {self.request.user.last_name}"}
        )
        serializer.save(patient=patient)

    def get_queryset(self):
        # Filter forms by the current user's patient profile
        if self.request.user.user_type == 'DOCTOR':
            return PatientForm.objects.all()
        return PatientForm.objects.filter(patient__user=self.request.user)

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [permissions.IsAdminUser()]

class ChatMessageViewSet(viewsets.ModelViewSet):
    serializer_class = ChatMessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):        
        queryset = ChatMessage.objects.all()
        patient_id = self.request.query_params.get('patient_id')
        doctor_id = self.request.query_params.get('doctor_id')

        # Filter based on user type
        if self.request.user.user_type == 'PATIENT':
            patient = Patient.objects.get(user=self.request.user)
            queryset = queryset.filter(patient=patient)
        elif self.request.user.user_type == 'DOCTOR':
            if patient_id:
                queryset = queryset.filter(patient_id=patient_id)
            if doctor_id:
                queryset = queryset.filter(doctor_id=doctor_id)

        return queryset

    def perform_create(self, serializer):
        if self.request.user.user_type == 'PATIENT':
            patient = Patient.objects.get(user=self.request.user)
            serializer.save(patient=patient, is_from_patient=True)
        elif self.request.user.user_type == 'DOCTOR':
            doctor = Doctor.objects.get(email=self.request.user.email)
            serializer.save(doctor=doctor, is_from_patient=False)
