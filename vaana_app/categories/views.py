from rest_framework.permissions import IsAuthenticated, AllowAny
from django.http import JsonResponse
from rest_framework.response import Response

from rest_framework import status

import json
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView

from .serializers import CategorySerializer
from .models import Category


class CategoryAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = CategorySerializer
    
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return JsonResponse({'categories': serializer.data}, safe=False, status=status.HTTP_200_OK)
        

    def post(self, request):
        payload = json.loads(request.body)
        user = request.user
        print(user)
        try:
            category = Category.objects.create(
                id=payload["id"],
                name=payload["name"],
                slug=payload["slug"],
                description=payload["description"],
                created_by=user,
                # products=payload["products"].set()
            )
            serializer = CategorySerializer(category)
            return JsonResponse({'categories': serializer.data}, safe=False, status=status.HTTP_201_CREATED)
        except ObjectDoesNotExist as e:
            return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)

class UpdateCategoryAPIView(APIView):
    permission_classes = (AllowAny, IsAuthenticated)
    serializer_class = CategorySerializer

    def put(self, request, category_id):
        user = request.user.id
        payload = json.loads(request.body)
        try:
            category_item = Category.objects.filter(created_by=user, id=category_id)
            # returns 1 or 0
            category_item.update(**payload)
            category = Category.objects.get(id=category_id)
            serializer = CategorySerializer(category)
            return JsonResponse({'category': serializer.data}, safe=False, status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)

class DeleteCategoryAPIView(APIView):
    permission_classes = (AllowAny, IsAuthenticated)
    serializer_class = CategorySerializer
    
    def delete(self, request, category_id):
        user = request.user.id
        try:
            category = Category.objects.get(created_by=user, id=category_id)
            category.delete()
            return Response('Success' ,status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist as e:
            return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)

