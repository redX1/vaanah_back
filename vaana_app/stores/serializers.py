from rest_framework import serializers
from .models import Store

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = [
            'id', 
            'name', 
            'created_at', 
            'created_by', 
            'store_address',
            "is_active",
        ]

