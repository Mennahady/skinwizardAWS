from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PatientViewSet, SkinImageViewSet, DiagnosisViewSet

router = DefaultRouter()
#router.register(r'patients', PatientViewSet)
router.register(r'images', SkinImageViewSet, basename='skin-image')
router.register(r'diagnoses', DiagnosisViewSet, basename='diagnosis')

urlpatterns = [
    path('', include(router.urls)),
]
