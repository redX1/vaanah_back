from rest_framework import serializers
from .models import Fund

class FundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fund
        fields = [
            'id',
            'amount',
            'customer',
            'payment',
            'order',
            'wallet',
            'payment_id',
            'status'
        ]