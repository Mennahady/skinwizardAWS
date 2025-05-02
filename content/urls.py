from django.urls import path
from .views import VlogListView, VlogDetailView, VlogCreateView

urlpatterns = [
    path('vlogs/', VlogListView.as_view(), name='vlog-list'),
    path('vlogs/<int:pk>/', VlogDetailView.as_view(), name='vlog-detail'),
    path('vlogs/create/', VlogCreateView.as_view(), name='vlog-create'),
]
