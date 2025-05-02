
# Register your models here.
from django.contrib import admin
from .models import SkinImage, Diagnosis


@admin.register(SkinImage)
class SkinImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('patient__name',)
    autocomplete_fields = ['patient']


@admin.register(Diagnosis)
class DiagnosisAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'image', 'diagnosis_1', 'confidence_1',
        'diagnosis_2', 'confidence_2', 'diagnosis_3', 'confidence_3', 'created_at'
    )
    list_filter = ('created_at',)
    search_fields = ('image__patient__name', 'diagnosis_1', 'diagnosis_2', 'diagnosis_3')
    autocomplete_fields = ['image']
