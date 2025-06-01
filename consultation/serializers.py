from rest_framework import serializers
from .models import Diagnosis, Message, ChatSession, ChatMessage
from patient_form.models import Patient
from django.contrib.auth import get_user_model

User = get_user_model()

class DiagnosisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnosis
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

class ChatSessionSerializer(serializers.ModelSerializer):
    patient_name = serializers.SerializerMethodField()
    doctor_name = serializers.SerializerMethodField()

    class Meta:
        model = ChatSession
        fields = ['id', 'patient', 'doctor', 'diagnosis', 'status', 'created_at', 'updated_at', 'patient_name', 'doctor_name']
        read_only_fields = ['created_at', 'updated_at']

    def get_patient_name(self, obj):
        return f"{obj.patient.name}" if obj.patient else None

    def get_doctor_name(self, obj):
        return f"{obj.doctor.first_name} {obj.doctor.last_name}" if obj.doctor else None

class ChatMessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField()

    class Meta:
        model = ChatMessage
        fields = ['id', 'session', 'sender', 'content', 'created_at', 'sender_name']
        read_only_fields = ['created_at']

    def get_sender_name(self, obj):
        if obj.sender.user_type == 'DOCTOR':
            return f"Dr. {obj.sender.first_name} {obj.sender.last_name}"
        return obj.sender.first_name
