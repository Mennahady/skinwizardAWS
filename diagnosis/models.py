from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from patient_form.models import Patient, PatientForm
from datetime import date

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

@receiver(post_save, sender=Diagnosis)
def create_patient_form(sender, instance, created, **kwargs):
    """Create a patient form after diagnosis is made"""
    if created:
        # Check if patient doesn't already have a form
        if not PatientForm.objects.filter(patient=instance.image.patient).exists():
            PatientForm.objects.create(
                patient=instance.image.patient,
                date_of_birth=date.today(),  # This will be updated by the patient
                gender='Other',  # Default value, to be updated by patient
                duration='Less than 1 month',  # Default value
                condition_frequency='Once',  # Default value
                affected_body_parts='Other'  # Default value
            )
