from rest_framework import generics, permissions
from .models import Vlog
from .serializers import VlogSerializer

class VlogListView(generics.ListAPIView):
    queryset = Vlog.objects.all().order_by('-created_at')
    serializer_class = VlogSerializer
    permission_classes = [permissions.AllowAny]  # Anyone can view vlogs

class VlogDetailView(generics.RetrieveAPIView):
    queryset = Vlog.objects.all()
    serializer_class = VlogSerializer
    permission_classes = [permissions.AllowAny]

class VlogCreateView(generics.CreateAPIView):
    queryset = Vlog.objects.all()
    serializer_class = VlogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(doctor=self.request.user)
