from rest_framework import serializers
from .models import Product, Review
from files.serializers import FileSerializer

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            "id",
            "title",
            "comment",
            "rating",
            "product",
            "user",
            "created_at",
            "updated_at",
        ]
class ProductSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True)
    images = serializers.ListField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "price",
            "category",
            "is_active",
            "quantity",
            "rating",
            "images",
            "created_by",
            "created_at",
            "updated_at",
            "store",
            "reviews",
        ]
    
    def create(self, validated_data):
        return Product.objects.create_user(**validated_data)
class ProductResponseSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True)
    images = FileSerializer(many=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "price",
            "category",
            "is_active",
            "quantity",
            "rating",
            "images",
            "created_by",
            "created_at",
            "updated_at",
            "store",
            "reviews",
        ]