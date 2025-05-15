from django.db import models
from django.conf import settings  # Correct way to get User model

class Patient(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='patient_profile',
        null=True  # Allow null temporarily for migration
    )
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class PatientForm(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='forms')
    date_of_birth = models.DateField()
    gender = models.CharField(
        max_length=10,
        choices=[
            ('Male', 'Male'),
            ('Female', 'Female'),
            ('Other', 'Other'),
        ]
    )
    duration = models.CharField(
        max_length=20,
        choices=[
            ('Less than 1 month', 'Less than 1 month'),
            ('1-6 months', '1-6 months'),
            ('More than 6 months', 'More than 6 months'),
        ]
    )
    condition_frequency = models.CharField(
        max_length=20,
        choices=[
            ('Once', 'Once'),
            ('1-3 times', '1-3 times'),
            ('More than 3 times', 'More than 3 times'),
        ]
    )
    affected_body_parts = models.CharField(
        max_length=20,
        choices=[
            ('Face', 'Face'),
            ('Arms', 'Arms'),
            ('Legs', 'Legs'),
            ('Other', 'Other'),
        ]
    )
    other_conditions = models.TextField(blank=True)
    additional_photo = models.ImageField(upload_to='patient_photos/', blank=True, null=True)

    def __str__(self):
        return f"Form for {self.patient.name}"

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class ChatMessage(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='messages')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='messages')
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_from_patient = models.BooleanField(default=True)

    def __str__(self):
        return f"Message from {'patient' if self.is_from_patient else 'doctor'} at {self.sent_at}"
