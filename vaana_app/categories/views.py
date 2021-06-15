from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.http import JsonResponse
from rest_framework.response import Response

from rest_framework import status

import json
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView

from .serializers import CategorySerializer
from .models import Category
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import permission_classes
from products.models import Product
from products.serializers import ProductSerializer
from django.utils.timezone import now

class CategoryAPIView(APIView):
    serializer_class = CategorySerializer
    
    def get(self, request):
        categories = Category.objects.exclude(parent__isnull=False)
        paginator = PageNumberPagination()

        page_size = 20
        paginator.page_size = page_size        
        page = paginator.paginate_queryset(categories, request)

        serializer = CategorySerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
        
    @csrf_exempt
    @permission_classes([IsAuthenticated])
    def post(self, request):
        payload = json.loads(request.body)
        user = request.user
        
        try:
            category = Category.objects.create(
                name=payload["name"],
                slug=payload["slug"],
                is_active= payload["is_active"],
                description=payload["description"],
                # parent=Category.objects.get(name=payload['parent']),
                created_by=user
            )
            serializer = CategorySerializer(category)
            return JsonResponse({'category': serializer.data}, safe=False, status=status.HTTP_201_CREATED)
        except ObjectDoesNotExist as e:
            return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)

class RetrieveDeleteUpdateCategoryAPIView(RetrieveUpdateAPIView):
    serializer_class = CategorySerializer

    def get(self, request, category_id):
        category = Category.objects.get(id=category_id)
        serializer = CategorySerializer(category)
        return JsonResponse({'category': serializer.data}, safe=False, status=status.HTTP_200_OK)

    @permission_classes([IsAuthenticated])
    def put(self, request, category_id):
        user = request.user.id
        payload = json.loads(request.body)
        try:
            category_item = Category.objects.filter(created_by=user, id=category_id)
            category_item.update(
                **payload,
                updated_at=now()
                )
            category = Category.objects.get(id=category_id)
            serializer = CategorySerializer(category)
            return JsonResponse({'category': serializer.data}, safe=False, status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)

    @permission_classes([IsAuthenticated])
    def delete(self, request, category_id):
        user = request.user.id
        try:
            category = Category.objects.get(created_by=user, id=category_id)
            category.delete()
            return Response('Success' ,status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist as e:
            return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)


class CategoryProductsAPIView(APIView):
    serializer_class = ProductSerializer

    def get(self, request, category_id):
        products = Product.objects.filter(category=category_id)
        paginator = PageNumberPagination()

        page_size = 20
        paginator.page_size = page_size        
        page = paginator.paginate_queryset(products, request)

        serializer = ProductSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


class CategoryActivatedAPIView(APIView):
    def get(self, request):
        categories = Category.objects.filter(is_active=True)
        paginator = PageNumberPagination()

        page_size = 20
        paginator.page_size = page_size        
        page = paginator.paginate_queryset(categories, request)

        serializer = CategorySerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

class CategoryDeactivatedAPIView(APIView):

    def get(self, request):
        categories = Category.objects.filter(is_active=False)
        paginator = PageNumberPagination()

        page_size = 20
        paginator.page_size = page_size        
        page = paginator.paginate_queryset(categories, request)

        serializer = CategorySerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

class LatestCategoryAPIView(APIView):
    def get(self, request):
        categories = Category.objects.filter(is_active=True)[0:2]
        paginator = PageNumberPagination()

        page_size = 20
        paginator.page_size = page_size        
        page = paginator.paginate_queryset(categories, request)

        serializer = CategorySerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

