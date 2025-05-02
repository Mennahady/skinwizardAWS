

# Register your models here.
from django.contrib import admin
from .models import User, PatientProfile, DoctorProfile, PharmacyProfile

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'role', 'is_staff', 'is_active')
    search_fields = ('email',)
    list_filter = ('role', 'is_staff', 'is_active')

@admin.register(PatientProfile)
class PatientProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name')

@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'id_number')

@admin.register(PharmacyProfile)
class PharmacyProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'pharmacy_name', 'address')
