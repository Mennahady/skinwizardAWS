from rest_framework import serializers
from .models import PatientForm, Doctor, ChatMessage

class PatientFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientForm
        fields = [
            'id', 'patient', 'date_of_birth', 'gender', 'duration',
            'condition_frequency', 'affected_body_parts',
            'other_conditions', 'additional_photo'
        ]

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['id', 'name', 'specialty', 'email', 'phone_number']

class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['id', 'patient', 'doctor', 'message', 'sent_at', 'is_from_patient']
