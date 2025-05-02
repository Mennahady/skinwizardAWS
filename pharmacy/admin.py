# Register your models here.
from django.contrib import admin
from .models import Medicine

@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'manufacturer', 'is_available', 'created_at')
    search_fields = ('name', 'manufacturer')
    list_filter = ('is_available',)
