from django.shortcuts import render
from rest_framework import status


from rest_framework.views import APIView
from rest_framework.generics import  RetrieveUpdateAPIView, ListAPIView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .backends import ShippoCarrierAPI

class ShippoCarrierAPIVIew(APIView):
    @csrf_exempt
    def get(self, request, *args, **kwargs):
        carrierApi = ShippoCarrierAPI()
        page = request.query_params.get('page')

        try:
            response = carrierApi.all(page)
            response = {
                'body': response.json(),
                'status': response.status_code
            }
        except Exception as e:
            response = {
                'body': str(e),
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR
            }

        return JsonResponse(response['body'], status=response['status'], safe=False)
