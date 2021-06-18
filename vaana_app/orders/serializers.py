from rest_framework import fields, serializers
from .models import Order, ShippingAddress

from addresses.serializers import AddressSerializer

class ShippingAddressSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = ShippingAddress
        fields = [
            "id",
            "phone_number",
            "notes",
            "address"
        ]

class OrderSerializer(serializers.ModelSerializer):
    shipping_address = ShippingAddressSerializer()
    class Meta:
        model = Order
        fields = [
            "id",
            "number",
            "cart",
            "user",
            "currency",
            "total_tax",
            "shipping_tax",
            "total_prices",
            "shipping_address",
            "shipping_method"
        ]

    def verify(self, **fields):
        for i in fields:
            if i in None:
                raise serializers.ValidationError(
                        i + 'field is required to initiate an order.'
                    )

    def validate(self, attrs):
        shipping_address = attrs.get('shipping_address', None)
        cart = attrs.get('cart', None)
        user = attrs.get('user', None)
        currency = attrs.get('currency', None)
        total_tax = attrs.get('total_tax', None)
        shipping_tax = attrs.get('shipping_tax', None)
        total_prices = attrs.get('total_prices', None)
        shipping_method = attrs.get('shipping_method', None)

        self.verify(cart, user, currency, total_tax, shipping_tax, total_prices, shipping_method, shipping_address)

    

