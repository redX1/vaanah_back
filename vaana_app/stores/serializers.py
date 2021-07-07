from rest_framework import serializers
from .models import Store
from products.serializers import ProductSerializer

class StoreSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

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

