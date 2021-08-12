from users.serializers import UserSerializer
from rest_framework import serializers
from .models import Store, StoreReview
from products.serializers import ProductResponseSerializer

class StoreReviewResultSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = StoreReview
        fields = [
            "id",
            "title",
            "comment",
            "rating",
            "store",
            "user",
            "created_at",
            "updated_at",
        ]
class StoreReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreReview
        fields = [
            "id",
            "title",
            "comment",
            "rating",
            "store",
            "user",
            "created_at",
            "updated_at",
        ]
        
class StoreSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Store
        fields = [
            'id', 
            'name', 
            'created_by', 
            'store_address',
            "is_active",
            "image",
            "rating",
            "created_by",
            "created_at",
            "updated_at",
        ]

class StoreResponseSerializer(serializers.ModelSerializer):
    products = ProductResponseSerializer(many=True)
    reviews = StoreReviewResultSerializer(many=True)
    class Meta:
        model = Store
        fields = [
            'id', 
            'name', 
            'created_by', 
            'store_address',
            "is_active",
            "image",
            "rating",
            "created_by",
            "created_at",
            "updated_at",
            "products",
            "reviews",

        ]
