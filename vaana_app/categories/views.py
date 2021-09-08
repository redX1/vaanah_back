from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from rest_framework.response import Response

from rest_framework import status

import json
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView

from .serializers import CategoryResultSerializer, CategorySerializer
from .models import Category
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import permission_classes
from products.models import Product
from products.serializers import ProductSerializer
from django.utils.timezone import now
from cores.utils import CustomPagination
from rest_framework.filters import SearchFilter
from django.db.models import Count

class CategorySearchAPIView(ListAPIView):
    serializer_class = CategoryResultSerializer
    queryset  = Category.objects.all()
    filter_backends =  [SearchFilter,]
    search_fields = ['name', 'description']

class CategoryUpdateDeleteAPIView(RetrieveUpdateAPIView):
    serializer_class = CategorySerializer

    def get(self, request, category_id):
        try:
            category = Category.objects.get(id=category_id)
            category.views += 1
            category.save()
            serializer = CategoryResultSerializer(category)
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
    def put(self, request, category_id):
        user = request.user
        payload = json.loads(request.body)
        response = {
            'body': {
                'error':'Unauthorized action'
            },
            'status': status.HTTP_403_FORBIDDEN
        }

        if user.is_superuser == True:
            try:
                category_item = Category.objects.filter(created_by=user, id=category_id)
                category_item.update(
                    **payload,
                    updated_at=now()
                    )
                category = Category.objects.get(id=category_id)
                serializer = CategoryResultSerializer(category)
                response['body'] = serializer.data
                response['status'] = status.HTTP_200_OK

            except ObjectDoesNotExist as e:
                response['body'] = {'error': str(e)}
                response['status'] = status.HTTP_404_NOT_FOUND

        return JsonResponse(response['body'], status=response['status'], safe=False)

    @permission_classes([IsAuthenticated])
    def delete(self, request, category_id):
        user = request.user
        response = {
            'body': {
                'error':'Unauthorized action'
            },
            'status': status.HTTP_403_FORBIDDEN
        }

        if user.is_superuser == True:
            try:
                category = Category.objects.get(created_by=user, id=category_id)
                category.delete()
                response['body'] = 'Success'
                response['status'] = status.HTTP_200_OK
            except ObjectDoesNotExist as e:
                response['body'] = {'error': str(e)}
                response['status'] = status.HTTP_404_NOT_FOUND

        return JsonResponse(response['body'], status=response['status'], safe=False)

class CategoryAPIView(APIView):
    def get(self, request):
        categories = Category.objects.filter(is_active=True)
        paginator = PageNumberPagination()

        page_size = 20
        paginator.page_size = page_size        
        page = paginator.paginate_queryset(categories, request)

        serializer = CategoryResultSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @csrf_exempt
    @permission_classes([IsAuthenticated])
    def post(self, request):
        payload = json.loads(request.body)
        user = request.user
        serializer = CategorySerializer(data=payload)
        serializer.is_valid(raise_exception=True)
        response = {
            'body': {
                'error':'Unauthorized action'
            },
            'status': status.HTTP_403_FORBIDDEN
        }

        if user.is_superuser == True:
            try:
                category = Category.objects.create(
                    name=payload["name"],
                    slug=payload["slug"],
                    is_active= payload["is_active"],
                    description=payload["description"],
                    parent = Category.objects.get(id=payload['parent']) if 'parent' in payload else None,
                    image= payload['image'],
                    created_by=user
                )
            
                response['body'] = CategoryResultSerializer(category).data
                response['status'] = status.HTTP_201_CREATED
                
            except Exception as e:
                response['body'] = {'error': str(e)}
                response['status'] = status.HTTP_500_INTERNAL_SERVER_ERROR
        
        return JsonResponse(response['body'], status=response['status'], safe=False)

class LatestCategoryAPIView(APIView):
    def get(self, request):
        categories = Category.objects.filter(is_active=True).order_by('-created_at')
        paginator = PageNumberPagination()

        page_size = 20
        paginator.page_size = page_size        
        page = paginator.paginate_queryset(categories, request)

        serializer = CategoryResultSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

class MostViewedCategoryAPIView(APIView):
    def get(self, request):
        categories = Category.objects.annotate(views_count=Count('views')).order_by('-views')
        paginator = PageNumberPagination()

        page_size = 20
        paginator.page_size = page_size        
        page = paginator.paginate_queryset(categories, request)

        serializer = CategoryResultSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

class CategoryProductsAPIView(APIView):
    def get(self, request, category_id):
        try:
            category = Category.objects.get(id=category_id, is_active=True)
            products = Product.objects.filter(category=category)
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

