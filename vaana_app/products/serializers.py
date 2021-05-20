from rest_framework import serializers
from .models import Product, Review



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
            "created_by",
            "created_at",
        ]
class ProductSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True)

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
            "created_by",
            "created_by",
            "created_at",
            "store",
            "reviews"
        ]
