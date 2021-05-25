from rest_framework.serializers import Serializer
from backend.vaana_app.carts.models import Cart
from backend.vaana_app.carts.serializers import CartSerializer
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


class CartAddView(APIView):

    @permission_classes([IsAuthenticated])
    def post(self, request, *args, **kwargs):
        user = request.user
        cart = Cart.objects.get(owner = user, status = Cart.OPEN)

        response = {
            'message': 'This user already have an open cart',
            'status': status.HTTP_400_BAD_REQUEST
        }

        if cart is None:
            serializer = CartSerializer(data=json.loads(request.body))

            response['message'] = 'This user already have an open cart'
            response['status'] = status.HTTP_400_BAD_REQUEST

            if serializer.is_valid():
                serializer.save()

                response['message'] = serializer.data
                response['status'] = status.HTTP_201_CREATED

        return JsonResponse(response['message'], status = response['status'])
