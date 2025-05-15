from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.shortcuts import get_object_or_404
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
    serializer_class = SkinImageSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Only return images belonging to the authenticated user
        return SkinImage.objects.filter(patient__user=self.request.user)
    
    def perform_create(self, serializer):
        # Get or create patient profile for the user
        patient = get_object_or_404(Patient, user=self.request.user)
        serializer.save(patient=patient)
    
    @action(detail=False, methods=['post'])
    def scan(self, request):
        """Handle real-time camera capture"""
        if 'image' not in request.FILES:
            return Response({'error': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)
            
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
    serializer_class = DiagnosisSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['image__patient__name']
    
    def get_queryset(self):
        # Only return diagnoses for the authenticated user's images
        return Diagnosis.objects.filter(image__patient__user=self.request.user)