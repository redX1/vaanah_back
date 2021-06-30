from django.db.models import Q
from django.http import Http404
from rest_framework.pagination import PageNumberPagination

from rest_framework.views import APIView
from rest_framework.generics import  RetrieveUpdateAPIView
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
        products = Product.objects.filter(is_active=True)
        paginator = PageNumberPagination()

        page_size = 20
        paginator.page_size = page_size        
        page = paginator.paginate_queryset(products, request)

        serializer = ProductSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @csrf_exempt
    @permission_classes([IsAuthenticated])
    def post(self, request):
        payload = json.loads(request.body)
        user = request.user