from django.db.models import Q
from django.http import Http404
from rest_framework.pagination import PageNumberPagination

from rest_framework.views import APIView
from rest_framework.generics import  RetrieveUpdateAPIView, ListAPIView
from rest_framework.response import Response

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import serializers, status
import json
from django.core.exceptions import ObjectDoesNotExist

from .models import Product, Category, Review, Store
from .serializers import ProductResponseSerializer, ProductSerializer, ReviewSerializer
from django.utils.timezone import now
from cores.utils import CustomPagination
from users.models import User
from files.models import File
from rest_framework.filters import SearchFilter
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models.functions import Greatest
from django.db import connection
with connection.cursor() as cursor:
    cursor.execute('CREATE EXTENSION IF NOT EXISTS pg_trgm')
class ProductSearchAPIView(ListAPIView):
    serializer_class = ProductResponseSerializer
    # queryset  = Product.objects.all()
    # filter_backends =  [SearchFilter,]
    # search_fields = ['name', 'description']
    def get(self, request):
        key = self.request.query_params.get('search')
        products = Product.objects.annotate(similarity=Greatest(TrigramSimilarity('name', key), TrigramSimilarity('description', key))).filter(similarity__gt=0.1).order_by('-similarity')
        paginator = PageNumberPagination()

        page_size = 20
        paginator.page_size = page_size        
        page = paginator.paginate_queryset(products, request)

        serializer = ProductResponseSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

class ProductAPIView(APIView):
    serializer_class = ProductSerializer

    def addImageToProduct(self, product, image_id):
        try:
            image = File.objects.get(id=image_id)
            product.images.add(image)
        except Exception:
            pass

    def get(self, request):
        products = Product.objects.filter(is_active=True)
        paginator = PageNumberPagination()

        page_size = 20
        paginator.page_size = page_size        
        page = paginator.paginate_queryset(products, request)

        serializer = ProductResponseSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @csrf_exempt
    @permission_classes([IsAuthenticated])
    def post(self, request):
        payload = json.loads(request.body)
        user = request.user
        serializer = ProductSerializer(data=payload)
        serializer.is_valid(raise_exception=True)
        response = {
            'body': {
                'error':'Unauthorized action'
            },
            'status': status.HTTP_403_FORBIDDEN
        }
        if user.account_type == User.SELLER:
            try:
                store = Store.objects.get(id=payload['store'], created_by= user)
                category = Category.objects.get(id=payload['category'])
                product = Product.objects.create(
                    category=category,
                    name=payload["name"],
                    slug=payload["slug"],
                    description=payload["description"],
                    price=payload["price"],
                    is_active= payload["is_active"],
                    quantity= payload["quantity"],
                    created_by=user,
                    store=store
                    )
                for i in payload['images']:
                    self.addImageToProduct(product, i)
                response['body'] = ProductResponseSerializer(product).data
                response['status'] = status.HTTP_201_CREATED
            except ObjectDoesNotExist as e:
                response['body'] = {'error': str(e)}
                response['status'] = status.HTTP_404_NOT_FOUND

        return JsonResponse(response['body'], status=response['status'], safe=False)

class SellerProductAPIView(APIView):
    @permission_classes([IsAuthenticated])
    def get(self, request):
        user = request.user
        products = Product.objects.filter(created_by=user)
        paginator = PageNumberPagination()
        paginator.page_size = 20        
        page = paginator.paginate_queryset(products, request)

        serializer = ProductResponseSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

class ProductUpdateDeleteAPIView(RetrieveUpdateAPIView):
    def get(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
            serializer = ProductResponseSerializer(product)
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
    def put(self, request, product_id):
        user = request.user
        payload = json.loads(request.body)
        try:
            product_item = Product.objects.filter(created_by=user, id=product_id)
            product_item.update(
                **payload,
                updated_at=now()
                )
            product = Product.objects.get(id=product_id)
            serializer = ProductResponseSerializer(product)
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
    def delete(self, request, product_id):
        user = request.user
        try:
            product = Product.objects.get(created_by=user, id=product_id)
            product.delete()
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

class LatestProductAPIView(APIView):
    def get(self, request):
        products = Product.objects.filter(is_active=True)[0:2]
        paginator = PageNumberPagination()

        page_size = 20
        paginator.page_size = page_size        
        page = paginator.paginate_queryset(products, request)

        serializer = ProductResponseSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

class ProductReviewsAPIView(APIView):
    serializer_class = ReviewSerializer

    def get(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id, is_active=True)
            reviews = Review.objects.filter(product=product)
            paginator = CustomPagination()
            paginator.page_size = 20        
            page = paginator.paginate_queryset(reviews, request)

            serializer = ReviewSerializer(page, many=True)
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

    @csrf_exempt
    @permission_classes([IsAuthenticated])
    def post(self, request):
        payload = json.loads(request.body)
        user = request.user
        serializer = ReviewSerializer(data=payload)
        serializer.is_valid(raise_exception=True)
        try:
            product = Product.objects.get(id=payload['product'])
            review = Review.objects.create(
                title=payload["title"],
                comment=payload["comment"],
                rating=payload["rating"],
                product=product,
                user=user
            )
            response = {
                'body': ReviewSerializer(review).data,
                'status': status.HTTP_201_CREATED
            }
        except Exception as e:
            response = {
                'body': {
                    'error': str(e)
                },
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR
            }
        return JsonResponse(response['body'], status=response['status'], safe=False)

class ReviewUpdateDeleteAPIView(RetrieveUpdateAPIView):
    def get(self, request, review_id):
        try:
            review = Review.objects.get(id=review_id)
            serializer = ReviewSerializer(review)
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
    def put(self, request, review_id):
        user = request.user
        payload = json.loads(request.body)
        try:
            review_item = Review.objects.filter(user=user, id=review_id)
            review_item.update(
                **payload,
                updated_at=now()
                )
            review = Review.objects.get(id=review_id)
            serializer = ReviewSerializer(review)
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
    def delete(self, request, review_id):
        user = request.user
        try:
            review = Review.objects.get(user=user, id=review_id)
            review.delete()
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
