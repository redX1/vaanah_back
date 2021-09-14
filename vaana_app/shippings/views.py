from .models import Shipment, Transaction
import json
from rest_framework import serializers, status


from rest_framework.views import APIView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .backends import ShippoCarrierAPI, ShippoShipmentAPI, ShippoTrackingAPI, ShippoTransactionAPI
from .serializers import ShippoShipmentSerializer, ShippoTransactionSerializer

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
            shipment = Shipment.objects.get(id=data['id'])
            shipment.object_id = apiResponse['object_id']
            shipment.save()
            response = {
                'body': {
                    'api_response': apiResponse,
                    'data': ShippoShipmentSerializer(shipment).data
                },
                'status': status.HTTP_201_CREATED
            }
        except Exception as e:
            response = {
                'body': str(e),
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR
            }        
        
        return JsonResponse(response['body'], status=response['status'], safe=False)

    @csrf_exempt
    def get(self, request, *args, **kwargs):
        shipmentApi = ShippoShipmentAPI()
        page = request.query_params.get('page')
        objects_id = request.query_params.get('objects_id')

        try:
            apiResponse = shipmentApi.retrieve(objects_id) if objects_id is not None else shipmentApi.all(page)
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

class ShippoTransactionAPIView(APIView):
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        playload = json.loads(request.body)
        serializer = ShippoTransactionSerializer(data=playload)
        serializer.is_valid(raise_exception=True)
        transactionApi = ShippoTransactionAPI()

        try:
            shipment = Shipment.objects.get(id=playload['shipment'])
            data = {
                'shipment': ShippoShipmentSerializer(shipment).data,
                'servicelevel_token': playload['servicelevel_token'],
                'carrier_account': playload['carrier_account']
            }
            serializer.save()
            apiResponse = transactionApi.create(data)
            transaction = Transaction.objects.get(id=serializer.data['id'])
            transaction.object_id = apiResponse['object_id']
            transaction.save()
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

    @csrf_exempt
    def get(self, request, *args, **kwargs):
        transactionApi = ShippoTransactionAPI()
        page = request.query_params.get('page')
        objects_id = request.query_params.get('objects_id')

        try:
            apiResponse = transactionApi.retrieve(objects_id) if objects_id is not None else transactionApi.all(page)
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

class ShippoTrackingAPIView(APIView):
    def get(self, request, carrier, tracking_number):
        trackingApi = ShippoTrackingAPI()
        try:
            apiResponse = trackingApi.get(carrier=carrier, tracking_number=tracking_number)
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

