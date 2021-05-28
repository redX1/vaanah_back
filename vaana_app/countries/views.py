from django.shortcuts import render
from requests import api

from rest_framework.views import APIView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
import json
from django.core.exceptions import ObjectDoesNotExist
import requests
from .models import *
from .serializers import *


class CountryView(APIView):

    @csrf_exempt
    def get(self, request, *args, **kwargs):
        api_response = requests.get('https://restcountries.eu/rest/v2/all')
        countries = Country.objects.all()
        
        if api_response.status_code == 200:
            body = api_response.json()
            if len(body) > len(countries):
                for item in body:
                    try:
                        country = Country.objects.create(name=item['name'], region=item['region'], sub_region=item['subregion'])

                        for i in item['topLevelDomain']:
                            print('tpd  ' + i)
                            #tpd = TopLevelDomain.objects.create(domain=i)
                            country.top_level_domains.create(domain=i)

                        for i in item['callingCodes']:
                            print('cc  ' +i)
                            #cc = CallingCode.objects.create(code=i)
                            country.calling_codes.create(code=i)

                        for i in item['currencies']:
                            print(i)
                            #currency = Currency.objects.create(code=i['code'], name=i['name'], symbol=i['symbol'])
                            country.currencies.create(code=i['code'], name=i['name'], symbol=i['symbol'])

                    except Exception:
                        pass
                    countries = Country.objects.all()
        
        
        serializer = CountrySerializer(countries, many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
