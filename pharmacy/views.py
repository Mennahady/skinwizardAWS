from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from .models import Medicine
from .serializers import MedicineSerializer

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff

class MedicineViewSet(viewsets.ModelViewSet):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
    permission_classes = [IsAdminUser]  # Only admins can manage medicine

