from rest_framework import serializers
from .models import Vlog

class VlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vlog
        fields = '__all__'
