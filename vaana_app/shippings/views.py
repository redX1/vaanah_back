from .models import Address
import json
from django.shortcuts import render
from rest_framework import serializers, status


from rest_framework.views import APIView
from rest_framework.generics import  RetrieveUpdateAPIView, ListAPIView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .backends import ShippoCarrierAPI, ShippoShipmentAPI
from .serializers import ShippoAddressSerializer, ShippoShipmentSerializer

class ShippoCarrierAPIVIew(APIView):
    @csrf_exempt
    def get(self, request, *args, **kwargs):
        carrierApi = ShippoCarrierAPI()
        page = request.query_params.get('page')

        try:
            apiResponse = carrierApi.all(page)
            response = {
                'body': apiResponse.json(),
                'status': apiResponse.status_code
            }
        except Exception as e:
            response = {
                'body': str(e),
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR
            }

        return JsonResponse(response['body'], status=response['status'], safe=False)

class ShippoShipmentAPIView(APIView):
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        playload = json.loads(request.body)
        shipmentSerializer = ShippoShipmentSerializer(data=playload)
        shipmentSerializer.is_valid(raise_exception=True)
        shipmentApi = ShippoShipmentAPI()

        try:
            shipmentSerializer.save()
            data = shipmentSerializer.data
            apiResponse = shipmentApi.create(data)
            response = {
                'body': apiResponse,
                'status': status.HTTP_201_CREATED
            }
        except Exception as e:
            response = {
                'body': str(e),
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR
            }        
        
        return JsonResponse(response['body'], status=response['status'], safe=False)

