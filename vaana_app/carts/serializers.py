from rest_framework import fields, serializers
from .models import Cart, CartItem

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = [
            "id",
            "product",
            "quantity",
        ]


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)
    class Meta:
        model = Cart
        fields = [
            "id",
            "owner",
            "status",
            "merged_date",
            "items",
        ]
