from rest_framework import viewsets , permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Patient, SkinImage, Diagnosis
from .serializers import PatientSerializer, SkinImageSerializer, DiagnosisSerializer
from .ai_model import diagnose_image
from rest_framework import filters

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

class SkinImageViewSet(viewsets.ModelViewSet):
    queryset = SkinImage.objects.all()
    serializer_class = SkinImageSerializer
    
#In case something goes wrong (bad image path, AI error, etc.)
@action(detail=True, methods=['post'])
def diagnose(self, request, pk=None):
    try:
        skin_image = self.get_object()

        # Check if this image has already been diagnosed
        if Diagnosis.objects.filter(image=skin_image).exists():
            return Response({'error': 'Diagnosis already exists for this image'}, status=400)

        image_path = skin_image.image.path
        predictions = diagnose_image(image_path)

        if not predictions or len(predictions) < 3:
            return Response({'error': 'Insufficient predictions returned'}, status=500)

        diagnosis = Diagnosis.objects.create(
            image=skin_image,
            diagnosis_1=predictions[0][0],
            confidence_1=predictions[0][1],
            diagnosis_2=predictions[1][0],
            confidence_2=predictions[1][1],
            diagnosis_3=predictions[2][0],
            confidence_3=predictions[2][1],
        )
        serializer = DiagnosisSerializer(diagnosis)
        return Response(serializer.data)

    except Exception as e:
        return Response({'error': str(e)}, status=500)


class DiagnosisViewSet(viewsets.ModelViewSet):
    queryset = Diagnosis.objects.all()
    serializer_class = DiagnosisSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['image__patient__name']