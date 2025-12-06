from rest_framework import serializers
from .models import Swing

class SwingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Swing
        fields = ['id', 'video', 'created_at', 'processed', 'analysis_data']
        read_only_fields = ['processed', 'analysis_data']
