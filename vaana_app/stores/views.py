from rest_framework.decorators import permission_classes
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.http import JsonResponse
from rest_framework.response import Response

from .serializers import StoreSerializer
from .models import Store
from rest_framework import status

from .models import Store
import json
from django.core.exceptions import ObjectDoesNotExist
from products.models import Product
from products.serializers import ProductSerializer
from rest_framework.views import APIView
from django.utils.timezone import now


class StoreAPIView(APIView):
    serializer_class = ProductSerializer

    def get(self, request):
        stores = Store.objects.all()
        serializer = StoreSerializer(stores, many=True)
        return JsonResponse({'stores': serializer.data}, safe=False, status=status.HTTP_200_OK)

    @permission_classes([IsAuthenticated])
    def post(self, request):
        payload = json.loads(request.body)
        user = request.user
        try:
            store = Store.objects.create(
                name=payload["name"],
                created_by=user,
                store_address=payload['store_address'],
                is_active= payload["is_active"]
            )
            serializer = StoreSerializer(store)
            return JsonResponse({'stores': serializer.data}, safe=False, status=status.HTTP_201_CREATED)
        except ObjectDoesNotExist as e:
            return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)


class RetrieveDeleteUpdateStoreAPIView(RetrieveUpdateAPIView):

    def get(self, request, store_id):
        stores = Store.objects.filter(id=store_id)
        serializer = StoreSerializer(stores, many=True)
        return JsonResponse({'store': serializer.data}, safe=False, status=status.HTTP_200_OK)


    @permission_classes([IsAuthenticated])
    def put(self, request, store_id):
        user = request.user.id
        payload = json.loads(request.body)
        try:
            store_item = Store.objects.filter(created_by=user, id=store_id)
            store_item.update(
                **payload,
                updated_at=now()
                )
            store = Store.objects.get(id=store_id)
            serializer = StoreSerializer(store)
            return JsonResponse({'store': serializer.data}, safe=False, status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)

    @permission_classes([IsAuthenticated])
    def delete(self, request, store_id):
        user = request.user.id
        try:
            store = Store.objects.get(created_by=user, id=store_id)
            store.delete()
            return Response('Success' ,status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist as e:
            return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)

class StoreProductsAPIView(APIView):
    serializer_class = ProductSerializer

    def get(self, request, store_id):
        products = Product.objects.filter(store=store_id)
        serializer = ProductSerializer(products, many=True)
        return JsonResponse({'store products': serializer.data}, safe=False, status=status.HTTP_200_OK)


class StoreActivatedAPIView(APIView):
    def get(self, request):
        stores = Store.objects.filter(is_active=True)
        serializer = StoreSerializer(stores, many=True)
        return JsonResponse({'activated stores': serializer.data}, safe=False, status=status.HTTP_200_OK)


class StoreDeactivatedAPIView(APIView):
    def get(self, request):
        stores = Store.objects.filter(is_active=False)
        serializer = StoreSerializer(stores, many=True)
        return JsonResponse({'deactivated stores': serializer.data}, safe=False, status=status.HTTP_200_OK)

class LatestStoreAPIView(APIView):
    def get(self, request):
        stores = Store.objects.filter(is_active=True)[0:2]
        serializer = StoreSerializer(stores, many=True)
        return JsonResponse({'latest stores': serializer.data}, safe=False, status=status.HTTP_200_OK)
