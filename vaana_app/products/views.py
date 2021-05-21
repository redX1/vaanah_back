from django.db.models import Q
from django.http import Http404

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

from .models import Product, Category, Review, Store
from .serializers import ProductSerializer, ReviewSerializer
from django.utils.timezone import now


class ProductAPIView(APIView):
    serializer_class = ProductSerializer

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return JsonResponse({'products': serializer.data}, safe=False, status=status.HTTP_200_OK)

    @csrf_exempt
    @permission_classes([IsAuthenticated])
    def post(self, request):
        payload = json.loads(request.body)
        user = request.user
        try:
            product = Product.objects.create(
                category=Category.objects.get(id=payload['category']),
                name=payload["name"],
                slug=payload["slug"],
                description=payload["description"],
                price=payload["price"],
                is_active= payload["is_active"],
                quantity= payload["quantity"],
                created_by=user,
                store=Store.objects.get(id=payload['store'])
            )
            serializer = ProductSerializer(product)
            return JsonResponse({'products': serializer.data}, safe=False, status=status.HTTP_201_CREATED)
        except ObjectDoesNotExist as e:
            return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)

class RetrieveDeleteUpdateProductAPIView(RetrieveUpdateAPIView):
    serializer_class = ProductSerializer

    def get(self, request, product_id):
        product = Product.objects.get(id=product_id)
        # print(product.avg_rating)
        serializer = ProductSerializer(product)
        return JsonResponse({'product': serializer.data}, safe=False, status=status.HTTP_200_OK)

    @permission_classes([IsAuthenticated])
    def update(self, request, product_id):
        user = request.user.id
        payload = json.loads(request.body)
        try:
            product_item = Product.objects.filter(created_by=user, id=product_id)
            product_item.update(
                **payload,
                updated_at=now()
                )
            product = Product.objects.get(id=product_id)
            serializer = ProductSerializer(product)
            return JsonResponse({'product': serializer.data}, safe=False, status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)

    @permission_classes([IsAuthenticated])
    def delete(self, request, product_id):
        user = request.user.id
        try:
            product = Product.objects.get(created_by=user, id=product_id)
            product.delete()
            return Response('Success' ,status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist as e:
            return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)


class ProductActivatedAPIView(APIView):
    def get(self, request):
        products = Product.objects.filter(is_active=True)
        serializer = ProductSerializer(products, many=True)
        return JsonResponse({'activated products': serializer.data}, safe=False, status=status.HTTP_200_OK)

class ProductDeactivatedAPIView(APIView):

    def get(self, request):
        products = Product.objects.filter(is_active=False)
        serializer = ProductSerializer(products, many=True)
        return JsonResponse({'deactivated products': serializer.data}, safe=False, status=status.HTTP_200_OK)


class LatestProductAPIView(APIView):
    def get(self, request):
        products = Product.objects.filter(is_active=True)[0:2]
        serializer = ProductSerializer(products, many=True)
        return JsonResponse({'latest products': serializer.data}, safe=False, status=status.HTTP_200_OK)

class ProductReviewsAPIView(APIView):
    serializer_class = ReviewSerializer

    def get(self, request, product_id):
        reviews = Review.objects.filter(product=product_id)
        serializer = ReviewSerializer(reviews, many=True)
        return JsonResponse({'product reviews': serializer.data}, safe=False, status=status.HTTP_200_OK)

class ReviewAPIView(APIView):
    serializer_class = ReviewSerializer

    def get(self, request):
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return JsonResponse({'reviews': serializer.data}, safe=False, status=status.HTTP_200_OK)

    @csrf_exempt
    @permission_classes([IsAuthenticated])
    def post(self, request):
        payload = json.loads(request.body)
        user = request.user
        try:
            review = Review.objects.create(
                title=payload["title"],
                comment=payload["comment"],
                rating=payload["rating"],
                product=Product.objects.get(id=payload['product']),
                user=user
            )
            serializer = ReviewSerializer(review)
            return JsonResponse({'review': serializer.data}, safe=False, status=status.HTTP_201_CREATED)
        except ObjectDoesNotExist as e:
            return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)

class RetrieveDeleteUpdateReviewAPIView(RetrieveUpdateAPIView):
    serializer_class = ReviewSerializer

    def get(self, request, review_id):
        review = Review.objects.get(id=review_id)
        serializer = ReviewSerializer(review)
        return JsonResponse({'review': serializer.data}, safe=False, status=status.HTTP_200_OK)

    @permission_classes([IsAuthenticated])
    def update(self, request, review_id):
        user = request.user.id
        payload = json.loads(request.body)
        try:
            review_item = Review.objects.filter(user=user, id=review_id)
            review_item.update(
                **payload,
                updated_at=now()
                )
            review = Review.objects.get(id=review_id)
            serializer = ReviewSerializer(review)
            return JsonResponse({'review': serializer.data}, safe=False, status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)

    @permission_classes([IsAuthenticated])
    def delete(self, request, review_id):
        user = request.user.id
        try:
            review = Review.objects.get(user=user, id=review_id)
            review.delete()
            return Response('Success' ,status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist as e:
            return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)

