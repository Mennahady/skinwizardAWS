from rest_framework import serializers
from .models import Patient, SkinImage, Diagnosis

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'name', 'created_at']

class SkinImageSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.name', read_only=True)
    image_url = serializers.ImageField(source='image', read_only=True)

    class Meta:
        model = SkinImage
        fields = ['id', 'image', 'image_url', 'patient_name', 'uploaded_at']
        read_only_fields = ['patient']  # Patient will be set automatically from the authenticated user

class DiagnosisSerializer(serializers.ModelSerializer):
    image_url = serializers.ImageField(source='image.image', read_only=True)
    patient_name = serializers.CharField(source='image.patient.name', read_only=True)

    class Meta:
        model = Diagnosis
        fields = ['id', 'image', 'image_url', 'patient_name',
                  'diagnosis_1', 'confidence_1',
                  'diagnosis_2', 'confidence_2',
                  'diagnosis_3', 'confidence_3',
                  'created_at']
