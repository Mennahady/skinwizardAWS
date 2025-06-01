from rest_framework import generics, permissions, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User
from .models import Diagnosis as ConsultationDiagnosis, Message, ChatSession, ChatMessage
from .serializers import DiagnosisSerializer, MessageSerializer, ChatSessionSerializer, ChatMessageSerializer
from diagnosis.models import Diagnosis as DiagnosisFromDiagnosis
from patient_form.models import PatientForm, Patient, Doctor

class ShareDiagnosisView(generics.CreateAPIView):
    queryset = ConsultationDiagnosis.objects.all()
    serializer_class = DiagnosisSerializer
    permission_classes = [permissions.IsAuthenticated]

class ChatListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(sender=user) | Message.objects.filter(receiver=user)

class SendMessageView(generics.CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

class ChatSessionViewSet(viewsets.ModelViewSet):
    serializer_class = ChatSessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'DOCTOR':
            try:
                doctor = Doctor.objects.get(email=user.email)
                return ChatSession.objects.filter(doctor=doctor)
            except Doctor.DoesNotExist:
                return ChatSession.objects.none() # Return empty queryset if no Doctor profile found
        return ChatSession.objects.filter(patient__user=user)

    @action(detail=False, methods=['post'])
    def start_from_diagnosis(self, request):
        """Start a chat session from a diagnosis"""
        diagnosis_id = request.data.get('diagnosis_id')
        try:
            # Get the diagnosis and related patient
            diagnosis = DiagnosisFromDiagnosis.objects.get(id=diagnosis_id)
            patient = diagnosis.image.patient
            
            # Check if patient form exists and is complete
            patient_form = PatientForm.objects.get(patient=patient)
            if not patient_form.is_complete():
                return Response({
                    'error': 'Please complete your patient form first',
                    'form_id': patient_form.id
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Create or get existing chat session
            chat_session, created = ChatSession.objects.get_or_create(
                patient=patient,
                diagnosis=diagnosis,
                defaults={'status': 'PENDING'}
            )
            
            serializer = self.get_serializer(chat_session)
            return Response(serializer.data)
            
        except DiagnosisFromDiagnosis.DoesNotExist:
            return Response({'error': 'Diagnosis not found'}, status=status.HTTP_404_NOT_FOUND)
        except PatientForm.DoesNotExist:
            return Response({'error': 'Patient form not found'}, status=status.HTTP_404_NOT_FOUND)

class ChatMessageViewSet(viewsets.ModelViewSet):
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ChatMessage.objects.filter(session_id=self.kwargs['session_pk'])
