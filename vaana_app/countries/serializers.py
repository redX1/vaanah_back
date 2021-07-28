from rest_framework import fields, serializers
from .models import TopLevelDomain, CallingCode, Currency, Country


class TopLevelDomainSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TopLevelDomain
        fields = [
            "id",
            "domain"
        ]

class CallinCodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = CallingCode
        fields = [
            "id",
            "code"
        ]

class CurrencySerializer(serializers.ModelSerializer):

    class Meta:
        model = Currency
        fields = [
            "id",
            "code",
            "name",
            "symbol"
        ]

class CountrySerializer(serializers.ModelSerializer):

    top_level_domains = TopLevelDomainSerializer(many=True)
    calling_codes = CallinCodeSerializer(many=True)
    currencies = CurrencySerializer(many=True)

    class Meta:
        model = Country
        fields = [
            "id",
            "name",
            "top_level_domains",
            "calling_codes",
            "region",
            "sub_region",
            "currencies"
        ]