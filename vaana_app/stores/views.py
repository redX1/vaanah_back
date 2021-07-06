from rest_framework.decorators import permission_classes
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from rest_framework.response import Response

from .serializers import StoreSerializer
from .models import Store
from rest_framework import serializers, status

import json
from django.core.exceptions import ObjectDoesNotExist
from products.models import Product
from products.serializers import ProductSerializer
from rest_framework.views import APIView
from django.utils.timezone import now
from rest_framework.filters import SearchFilter
from cores.utils import CustomPagination
from users.models import User

class StoreSearchAPIView(ListAPIView):
    serializer_class = StoreSerializer
    queryset  = Store.objects.all()
    filter_backends =  [SearchFilter,]
    search_fields = ['^name', ]

class LatestStoreAPIView(APIView):
    def get(self, request):
        stores = Store.objects.filter(is_active=True)[0:2]
        paginator = PageNumberPagination()

        page_size = 20
        paginator.page_size = page_size        
        page = paginator.paginate_queryset(stores, request)

        serializer = StoreSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

class StoreAPIView(APIView):
    def get(self, request):
        stores = Store.objects.filter(is_active=True)
        paginator = PageNumberPagination()

        page_size = 20
        paginator.page_size = page_size        
        page = paginator.paginate_queryset(stores, request)

        serializer = StoreSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @permission_classes([IsAuthenticated])
    def post(self, request):
        payload = json.loads(request.body)
        user = request.user
        serializer = StoreSerializer(data=payload)
        serializer.is_valid(raise_exception=True)
        response = {
            'body': {
                'error':'Unauthorized action'
            },
            'status': status.HTTP_403_FORBIDDEN
        }
        if user.account_type == User.SELLER:
            try:
                store = Store.objects.create(
                    name=payload["name"],
                    created_by=user,
                    store_address=payload['store_address'],
                    is_active= payload["is_active"]
                )
                serializer = StoreSerializer(store)
                response['body'] = serializer.data
                response['status'] = status.HTTP_201_CREATED
            except Exception as e:
                response['body'] = {'error': str(e)}
                response['status'] = status.HTTP_500_INTERNAL_SERVER_ERROR
        
        return JsonResponse(response['body'], status=response['status'], safe=False)

class StoreProductsAPIView(APIView):
    serializer_class = ProductSerializer

    
    def get(self, request, store_id):
        try:
            store = Store.object.get(id=store_id, is_active=True)
            products = Product.objects.filter(store=store)
            paginator = CustomPagination()

            paginator.page_size = 20        
            page = paginator.paginate_queryset(products, request)

            serializer = ProductSerializer(page, many=True)
            response = {
                'body': paginator.get_paginated_response(serializer.data),
                'status': status.HTTP_200_OK
            }
        except ObjectDoesNotExist as e:
            response = {
                'body': {
                    'error': str(e)
                },
                'status': status.HTTP_404_NOT_FOUND
            }
        return JsonResponse(response['body'], status=response['status'], safe=False)

class StoreUpdateDeleteAPIView(RetrieveUpdateAPIView):
    def get(self, request, store_id):
        try:
            store = Store.objects.get(id=store_id, is_active=True)
            serializer = StoreSerializer(store)
            response = {
                'body': serializer.data,
                'status': status.HTTP_200_OK
            }
        except ObjectDoesNotExist as e:
            response = {
                'body': {
                    'error': str(e)
                },
                'status': status.HTTP_404_NOT_FOUND
            }
        return JsonResponse(response['body'], status=response['status'], safe=False)
        
    @permission_classes([IsAuthenticated])
    def put(self, request, store_id):
        user = request.user
        payload = json.loads(request.body)
        try:
            store_item = Store.objects.filter(created_by=user, id=store_id)
            store_item.update(
                **payload,
                updated_at=now()
                )
            store = Store.objects.get(id=store_id)
            serializer = StoreSerializer(store)
            response = {
                'body': serializer.data,
                'status': status.HTTP_200_OK
            }
        except ObjectDoesNotExist as e:
            response = {
                'body': {
                    'error': str(e)
                },
                'status': status.HTTP_404_NOT_FOUND
            }
        
        return JsonResponse(response['body'], status=response['status'], safe=False)

    @permission_classes([IsAuthenticated])
    def delete(self, request, store_id):
        user = request.user.id
        try:
            store = Store.objects.get(created_by=user, id=store_id)
            store.delete()
            response = {
                'body': 'Success',
                'status': status.HTTP_200_OK
            }
        except ObjectDoesNotExist as e:
            response = {
                'body': {
                    'error': str(e)
                },
                'status': status.HTTP_404_NOT_FOUND
            }
        return JsonResponse(response['body'], status=response['status'], safe=False)

class SellerStoreAPIView(APIView):
    @permission_classes([IsAuthenticated])
    def get(self, request):
        user = request.user
        stores = Store.objects.filter(created_by=user)
        paginator = PageNumberPagination()
        paginator.page_size = 20        
        page = paginator.paginate_queryset(stores, request)
        serializer = StoreSerializer(page, many=True)

        return paginator.get_paginated_response(serializer.data)
