from django.db import models
from patient_form.models import Patient  # Correct import (now Patient is in patient/models.py)

class SkinImage(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='skin_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.patient.name} at {self.uploaded_at}"

class Diagnosis(models.Model):
    image = models.ForeignKey(SkinImage, on_delete=models.CASCADE, related_name='diagnoses')
    diagnosis_1 = models.CharField(max_length=100)
    confidence_1 = models.FloatField()
    diagnosis_2 = models.CharField(max_length=100)
    confidence_2 = models.FloatField()
    diagnosis_3 = models.CharField(max_length=100)
    confidence_3 = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Diagnosis for {self.image.patient.name}"
