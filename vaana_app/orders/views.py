from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
import json
from django.core.exceptions import ObjectDoesNotExist
from .utils import Util

class OrderApiView(APIView):
    def get(self, *args, **kwargs):
        return JsonResponse(Util.getOrderNumber(), status=status.HTTP_200_OK, safe=False)