from logging import exception
from rest_framework.serializers import Serializer
from .models import WishList, WishListItem
from .serializers import WishListSerializer, WishListItemSerializer
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
import json
from django.core.exceptions import ObjectDoesNotExist
from products.models import Product


from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class WishListAddView(APIView):

    @swagger_auto_schema(
        operation_description="apiview post description override",
        request_body=WishListSerializer,
        security=[],
        tags=['WishLists'],
    )
    @csrf_exempt
    @permission_classes([IsAuthenticated])
    def post(self, request, *args, **kwargs):
        user = request.user

        response = {
            'body': {
                'error': 'This user already have an open wishlist'
            },
            'status': status.HTTP_400_BAD_REQUEST
        }

        try:
            wishlist = WishList.objects.get(owner = user)
            response ['body']['data'] = WishListSerializer(wishlist).data
            
        except Exception:
            try:
                wishlist = WishList.objects.create(owner=user)
                serializer = WishListSerializer(wishlist)
                response['body'] = serializer.data
                response['status'] = status.HTTP_201_CREATED

            except Exception as exception:
                response['body']['error'] = str(exception)
                response['status'] = status.HTTP_500_INTERNAL_SERVER_ERROR  

        return JsonResponse(response['body'], status = response['status'])

    @swagger_auto_schema(
        operation_description="apiview post description override",
        security=[],
        tags=['WishLists'],
    )
    @permission_classes([IsAuthenticated])
    def get(self, request, *args, **kwargs):
        user = request.user
        
        try:
            wishlist = WishList.objects.get(owner = user)
            response = {
                'body': WishListSerializer(wishlist).data,
                'status': status.HTTP_200_OK
            }
        except Exception:
            try:
                wishlist = WishList.objects.create(owner=user)
                serializer = WishListSerializer(wishlist)
                response = {
                    'body': serializer.data,
                    'status': status.HTTP_200_OK
                }
            except Exception as exception:
                response = {
                    'body': {
                        'error': str(exception)
                    },
                    'status': status.HTTP_500_INTERNAL_SERVER_ERROR
                }

        return JsonResponse(response['body'], status = response['status']) 

        
class WishListItemView(APIView):
    @swagger_auto_schema(
        operation_description="apiview post description override",
        request_body=WishListItemSerializer,
        security=[],
        tags=['WishLists'],
    )
    @csrf_exempt
    @permission_classes([IsAuthenticated])
    def post(self, request, *args, **kwargs):
        user = request.user
        payload = json.loads(request.body)
        serializer = WishListItemSerializer(data=payload)
        serializer.is_valid(raise_exception=True)

        product = Product.objects.get(id=payload['product'])
        response = {
            'body': {
                'error': 'Action not allowed'
            },
            'status': status.HTTP_401_UNAUTHORIZED
        }

        try:
            wishlist = WishList.objects.get(owner=user)
        except ObjectDoesNotExist:
            wishlist = WishList.objects.create(owner=user)

        if (wishlist.items.filter(product=product).exists()):
            response['body']['error'] = 'Already in wishlist'
            response['status'] = status.HTTP_401_UNAUTHORIZED
        
        else:
            item = WishListItem.objects.create(product=product) 
            wishlist.items.add(item)

            response['body'] = WishListSerializer(wishlist).data
            response['status'] = status.HTTP_201_CREATED
                        
        return JsonResponse(response['body'], status = response['status'], safe=False)


class WishListItemUpdateView(RetrieveUpdateAPIView):

    @permission_classes([IsAuthenticated])
    def update(self, request, id):
        user = request.user
        payload = json.loads(request.body)
        serializer = WishListItemSerializer(data=payload)
        serializer.is_valid(raise_exception=True)

        product = Product.objects.get(id=payload['product'])
        response = {
            'body': {
                'error': 'Action not allowed'
            },
            'status': status.HTTP_400_BAD_REQUEST
        }
        try:
            wishlist = WishList.objects.get(owner=user)
                    
            try:
                wishlist_item = WishListItem.objects.get(id=id)
                wishlist_item.save()
                response['body'] = WishListSerializer(wishlist).data
                response['status'] = status.HTTP_200_OK
            except ObjectDoesNotExist as e:
                response['body']['error'] = 'Item not founded'
                response['status'] = status.HTTP_404_NOT_FOUND
        except ObjectDoesNotExist as e:
            response['body']['error'] = 'Any opened wishlist founded'
            response['status'] = status.HTTP_400_BAD_REQUEST
  
        return JsonResponse(response['body'], status = response['status'], safe=False)

    @csrf_exempt
    @permission_classes([IsAuthenticated])
    def delete(self, request, id):
        user = request.user

        try:
                
            wishlist = WishList.objects.get(owner=user)
            try:
                wishlist_item = WishListItem.objects.get(id=id)
                wishlist.items.remove(wishlist_item)
                response = {
                    'body': WishListSerializer(wishlist).data,
                    'status': status.HTTP_200_OK
                }
            except ObjectDoesNotExist:
                response = {
                    'body': {
                    'error': 'WishList item not founded'
                    },
                    'status': status.HTTP_404_NOT_FOUND
                }

        except ObjectDoesNotExist:
            response = {
                'body': {
                    'error': 'Any open wishlist founded'
                },
                'status': status.HTTP_404_NOT_FOUND
            }

        return JsonResponse(response['body'], status = response['status'], safe=False)

