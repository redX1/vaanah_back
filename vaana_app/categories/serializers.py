from rest_framework import serializers
from .models import Category
from products.serializers import ProductSerializer

class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data

class CategorySerializer(serializers.ModelSerializer):
    # products = ProductSerializer(many=True)
    children = RecursiveField(many=True,allow_null=True)
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "parent",
            "is_active",
            "created_by",
            "created_at",
            "updated_at",
            "children",
            # "products",
        ]
