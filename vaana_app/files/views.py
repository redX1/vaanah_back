from datetime import datetime
from rest_framework.decorators import permission_classes
from rest_framework.parsers import MultiPartParser
from django.db.models.expressions import F
from django.shortcuts import render
from .models import File
from .serializers import FileSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import serializers, status
import json
from .utils import Util

class FileUploadAPIView(APIView):
    parser_classes = (MultiPartParser, )
    @csrf_exempt
    @permission_classes([IsAuthenticated])
    def post(self, request, *args, **kwargs):
        user = request.user
        payload = request.FILES
        serializer = FileSerializer(data=payload)
        serializer.is_valid(raise_exception=True)
        name = payload['file'].name.split('.')
        payload['file'].name = str(datetime.timestamp(datetime.now())) + Util.getRandomString() +'.' + name[1] 

        file = File(file=payload['file'], user=user)
        file.save()


        return JsonResponse(FileSerializer(file).data, status=status.HTTP_200_OK, safe=False)
