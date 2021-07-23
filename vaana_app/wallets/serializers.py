from django.db.models import fields
from .models import Wallet
from rest_framework import serializers
from funds.serializers import FundSerializer

class WalletSerializer(serializers.ModelSerializer):
    funds = FundSerializer(many=True)
    class Meta:
        model = Wallet
        fields = [
            'id',
            'seller',
            'funds',
        ]