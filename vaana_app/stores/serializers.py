from rest_framework import serializers
from .models import Store
from products.serializers import ProductResponseSerializer

class StoreSerializer(serializers.ModelSerializer):
    products = ProductResponseSerializer(many=True)

    class Meta:
        model = Store
        fields = [
            'id', 
            'name', 
            'created_by', 
            'store_address',
            "is_active",
            "image",
            "created_by",
            "created_at",
            "updated_at",
            "products",
        ]

