from django.db.models import fields
from rest_framework import serializers
from .models import ShippingMethod


class ShippingMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingMethod
        fields = [
            "id",
            "name",
            "price",
            "currency"
        ]