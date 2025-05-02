from rest_framework import viewsets
from .models import PatientForm, Doctor, ChatMessage
from .serializers import PatientFormSerializer, DoctorSerializer, ChatMessageSerializer

class PatientFormViewSet(viewsets.ModelViewSet):
    queryset = PatientForm.objects.all()
    serializer_class = PatientFormSerializer

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

class ChatMessageViewSet(viewsets.ModelViewSet):
    serializer_class = ChatMessageSerializer

    def get_queryset(self):        
        #filtering by patient_id and/or doctor_id.
        queryset = ChatMessage.objects.all()
        patient_id = self.request.query_params.get('patient_id')
        doctor_id = self.request.query_params.get('doctor_id')

        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
        if doctor_id:
            queryset = queryset.filter(doctor_id=doctor_id)

        return queryset
