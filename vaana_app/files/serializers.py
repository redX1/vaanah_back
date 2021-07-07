from .models import File
from rest_framework import fields, serializers

class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        fields = '__all__'

