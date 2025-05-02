from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PatientFormViewSet, DoctorViewSet, ChatMessageViewSet

router = DefaultRouter()
router.register(r'forms', PatientFormViewSet)
router.register(r'doctors', DoctorViewSet)
router.register(r'messages', ChatMessageViewSet, basename='chatmessage')

urlpatterns = [
    path('', include(router.urls)),
]