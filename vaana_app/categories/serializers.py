from rest_framework import serializers
from .models import Category
from products.serializers import ProductSerializer

class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "created_by",
            "products",
        ]
