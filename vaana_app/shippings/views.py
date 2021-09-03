from django.shortcuts import render
from rest_framework import status


from rest_framework.views import APIView
from rest_framework.generics import  RetrieveUpdateAPIView, ListAPIView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import shippo

''' class ShipmentAPIVIew(APIView):
    @csrf_exempt
    def get(self, *args, **kwargs):
        shippo.config.api_key = 'shippo_test_d88dfb2c748b3c9ea2483bded12428024b5f36e3'

        try:
            response = {
                'body': shippo.CarrierAccount.all(),
                'status': status.HTTP_200_OK
            }
        except Exception as e:
            response = {
                'body': str(e),
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR
            }

        return JsonResponse(response['body'], status=response['status'], safe=False) '''
