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
                wishlist = Wishlist.objects.create(owner=user)
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
        tags=['Wishlists'],
    )
    @permission_classes([IsAuthenticated])
    def get(self, request, *args, **kwargs):
        user = request.user
        
        try:
            wishlist = Wishlist.objects.get(owner = user)
            response = {
                'body': WishListSerializer(wishlist).data,
                'status': status.HTTP_200_OK
            }
        except Exception:
            try:
                wishlist = Wishlist.objects.create(owner=user)
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
            'status': status.HTTP_400_BAD_REQUEST
        }

        try:
            wishlist = WishList.objects.get(owner=user)
        except ObjectDoesNotExist:
            wishlist = WishList.objects.create(owner=user)

        item = WishListItem.objects.create(product=product)
                
        wishlist.items.add(item)
        response['body'] = WishListSerializer(wishlist).data
        response['status'] = status.HTTP_201_CREATED
                    
        return JsonResponse(response['body'], status = response['status'])


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
                wishlist_item.quantity = quantity
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


# from django.shortcuts import render
# from rest_framework.views import APIView
# from wishlist.serializers import WishListSerializer
# from .models import WishList
# from rest_framework.pagination import PageNumberPagination
# from rest_framework.decorators import permission_classes
# from rest_framework.permissions import IsAuthenticated, AllowAny
# from django.http import JsonResponse
# from rest_framework import status
# import json
# from django.core.exceptions import ObjectDoesNotExist
# from products.models import Product
# from django.utils.timezone import now

# # Create your views here.
# class WishListAPIView(APIView):
#     serializer_class = WishListSerializer

#     @permission_classes([IsAuthenticated])
#     def get(self, request):
#         wishlist = WishList.objects.filter(owner=request.user)
#         paginator = PageNumberPagination()

#         page_size = 20
#         paginator.page_size = page_size        
#         page = paginator.paginate_queryset(wishlist, request)

#         serializer = WishListSerializer(page, many=True)
#         return paginator.get_paginated_response(serializer.data)


#     @permission_classes([IsAuthenticated])
#     def post(self, request):
#         payload = json.loads(request.body)
#         user = request.user
#         if user.account_type == 'CUSTOMER':
#             try:
#                 store = WishList.objects.create(
#                     product= Product.objects.get(id=payload['product']),
#                     owner=user,
#                 )
#                 serializer = WishListSerializer(store)
#                 return JsonResponse({'store': serializer.data}, safe=False, status=status.HTTP_201_CREATED)
#             except ObjectDoesNotExist as e:
#                 return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
#         else:
#             return JsonResponse({'error':'You are not a Customer !'}, status=status.HTTP_403_FORBIDDEN)
 

# class RetrieveDeleteUpdateWishListAPIView(APIView):
#     def get(self, request, store_id):
#         wishlist = WishList.objects.filter(id=store_id)
#         serializer = WishListSerializer(wishlist, many=True)
#         return JsonResponse({'store': serializer.data}, safe=False, status=status.HTTP_200_OK)


#     @permission_classes([IsAuthenticated])
#     def put(self, request, store_id):
#         user = request.user.id
#         payload = json.loads(request.body)
#         try:
#             store_item = WishList.objects.filter(created_by=user, id=store_id)
#             store_item.update(
#                 **payload,
#                 updated_at=now()
#                 )
#             store = WishList.objects.get(id=store_id)
#             serializer = WishListSerializer(store)
#             return JsonResponse({'store': serializer.data}, safe=False, status=status.HTTP_200_OK)
#         except ObjectDoesNotExist as e:
#             return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)

#     @permission_classes([IsAuthenticated])
#     def delete(self, request, store_id):
#         user = request.user.id
#         try:
#             store = WishList.objects.get(created_by=user, id=store_id)
#             store.delete()
#             return Response('Success' ,status=status.HTTP_204_NO_CONTENT)
#         except ObjectDoesNotExist as e:
#             return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)

