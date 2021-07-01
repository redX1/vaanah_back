from rest_framework import serializers
from .models import WishList, WishListItem
from products.serializers import ProductSerializer

class WishListItemSerializer(serializers.ModelSerializer):

  class Meta:
        model = WishListItem
        fields = [
            "id",
            "product",
            "created_at",
            "updated_at",
        ]


class WishListSerializer(serializers.ModelSerializer):
    items = WishListItemSerializer(many=True)
    class Meta:
        model = WishList
        fields = [
            "id",
            "owner",
            "items",
            "created_at",
            "updated_at",
        ]
