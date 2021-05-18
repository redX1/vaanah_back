from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "get_absolute_url",
            "description",
            "price",
            "category",
            "date_added",
            "created_by",
        ]


