from django.db.models import Q
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
import json
from django.core.exceptions import ObjectDoesNotExist

from .models import Product, Category
from .serializers import ProductSerializer


class ProductAPIView(APIView):
    permission_classes = (AllowAny,IsAuthenticated)
    serializer_class = ProductSerializer

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return JsonResponse({'products': serializer.data}, safe=False, status=status.HTTP_200_OK)

    
    def post(self, request):
        payload = json.loads(request.body)
        user = request.user
        try:
            product = Product.objects.create(
                id=payload["id"],
                category=Category.objects.get(id=payload['category']),
                name=payload["name"],
                slug=payload["get_absolute_url"],
                description=payload["description"],
                price=payload["price"],
                date_added=payload["date_added"],
                created_by=user,
            )
            serializer = ProductSerializer(product)
            return JsonResponse({'products': serializer.data}, safe=False, status=status.HTTP_201_CREATED)
        except ObjectDoesNotExist as e:
            return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)

class UpdateProductAPIView(APIView):
    permission_classes = (AllowAny,IsAuthenticated)
    serializer_class = ProductSerializer

    def update(self, request, product_id):
        user = request.user.id
        payload = json.loads(request.body)
        try:
            product_item = Product.objects.all()
            # returns 1 or 0
            product_item.update(**payload)
            product = Product.objects.get(id=product_id)
            serializer = ProductSerializer(product)
            return JsonResponse({'product': serializer.data}, safe=False, status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)

class DeleteProductAPIView(APIView):
    permission_classes = (AllowAny,IsAuthenticated)
    serializer_class = ProductSerializer

    def delete(self, request, product_id):
        user = request.user.id
        try:
            product = Product.objects.get(created_by=user, id=product_id)
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist as e:
            return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)

