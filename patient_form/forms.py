from rest_framework import serializers  # type: ignore
from .models import PatientForm

class PatientFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientForm
        fields = [
            'id', 'patient', 'date_of_birth', 'gender', 'duration',
            'condition_frequency', 'affected_body_parts', 'other_conditions',
            'additional_photo'
        ]
        