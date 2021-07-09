from rest_framework import fields, serializers
from .models import Order, ShippingAddress

from addresses.serializers import AddressSerializer
from shippings.serializers import ShippingMethodSerializer
from carts.models import Cart
from carts.serializers import CartDetailsSerializer
from products.serializers import ProductResponseSerializer

class ShippingAddressSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = ShippingAddress
        fields = [
            "id",
            "phone_number",
            "notes",
            "address",
            "created_at",
            "updated_at",
        ]

class OrderSerializer(serializers.ModelSerializer):
    shipping_address = ShippingAddressSerializer()
    shipping_method = ShippingMethodSerializer()
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
            "shipping_method",
            "status",
            "created_at",
            "updated_at",
        ]

    def verify(self, fields):
        for i in fields:
            if i is None:
                raise serializers.ValidationError(
                        i + 'field is required to initiate an order.'
                    )


    def validate(self, attrs):
        shipping_address = attrs.get('shipping_address', None)
        cart = attrs.get('cart', None)
        currency = attrs.get('currency', None)
        total_tax = attrs.get('total_tax', None)
        shipping_tax = attrs.get('shipping_tax', None)
        total_prices = attrs.get('total_prices', None)
        shipping_method = attrs.get('shipping_method', None)

        self.verify([cart, currency, total_tax, shipping_tax, total_prices, shipping_method, shipping_address])

        if cart.status != Cart.OPEN:
            raise serializers.ValidationError(
                'Cart not founded' 
            )

        return {
            'shipping_address': shipping_address,
            'cart': cart,
            'currency': currency,
            'total_tax': total_tax,
            'shipping_tax': shipping_tax,
            'total_prices': total_prices,
            'shipping_method': shipping_method
        }


class SellerOrderSerializer(serializers.Serializer):
    shipping_address = ShippingAddressSerializer()
    shipping_method = ShippingMethodSerializer()
    products = ProductResponseSerializer(many=True)
    class Meta:
        fields = [
            "id",
            "number",
            "products"
            "user",
            "currency",
            "total_tax",
            "shipping_tax",
            "total_prices",
            "shipping_address",
            "shipping_method",
            "status",
            "created_at",
            "updated_at",
        ]
    
class OrderDetailsSerializer(serializers.ModelSerializer):
    shipping_address = ShippingAddressSerializer()
    shipping_method = ShippingMethodSerializer()
    cart = CartDetailsSerializer()
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
            "shipping_method",
            "status",
            "created_at",
            "updated_at",
        ]
