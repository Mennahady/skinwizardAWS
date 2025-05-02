from django.contrib import admin
from .models import Patient, PatientForm, Doctor, ChatMessage


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user', 'created_at')
    search_fields = ('name', 'user__email')
    list_filter = ('created_at',)


@admin.register(PatientForm)
class PatientFormAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'date_of_birth', 'gender', 'duration', 'condition_frequency', 'affected_body_parts')
    list_filter = ('gender', 'duration', 'condition_frequency', 'affected_body_parts')
    search_fields = ('patient__name',)
    autocomplete_fields = ['patient']


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'specialty', 'email', 'phone_number')
    search_fields = ('name', 'email', 'specialty')


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'doctor', 'sent_at', 'is_from_patient')
    list_filter = ('is_from_patient', 'sent_at')
    search_fields = ('patient__name', 'doctor__name', 'message')
    autocomplete_fields = ['patient', 'doctor']


# Register your models here.
