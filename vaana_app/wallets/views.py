from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import serializers, status
import json
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from users.models import User
from .models import Wallet
from .serializers import WalletSerializer

class WalletAPIView(APIView):
    @csrf_exempt
    @permission_classes([IsAuthenticated])
    def post(self, request, *args, **kwargs):
        user = request.user
        response = {
            'body': {
                'error':'Unauthorized action'
            },
            'status': status.HTTP_403_FORBIDDEN
        }
        if user.account_type == User.SELLER:
            wallet = Wallet.objects.create(seller=user)
            response['body'] = WalletSerializer(wallet)
            response['status'] = status.HTTP_201_CREATED

        return JsonResponse(response['body'], status = response['status'], safe=False)

    @csrf_exempt
    @permission_classes([IsAuthenticated])
    def get(self, request, *args, **kwargs):
        user = request.user
        response = {
            'body': {
                'error':'Unauthorized action'
            },
            'status': status.HTTP_403_FORBIDDEN
        }
        if user.account_type == User.SELLER:
            try:
                wallet = Wallet.objects.get(seller=user)
            except ObjectDoesNotExist:
                wallet = Wallet.objects.create(seller=user)
            
            response['body'] = WalletSerializer(wallet)
            response['status'] = status.HTTP_201_CREATED
        
        return JsonResponse(response['body'], status = response['status'], safe=False)
