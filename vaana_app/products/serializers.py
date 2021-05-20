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
            "created",
            "updated"
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
            "date_added",
            "last_updated",
            "created_by",
            "store",
            "reviews"
        ]
