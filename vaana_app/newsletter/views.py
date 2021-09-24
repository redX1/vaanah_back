import json
from rest_framework.fields import JSONField
from .models import Newsletter
from .serializers import NewsletterSerializer
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django.http import JsonResponse
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist

class NewsletterAPIView(APIView):
    serializer_class = NewsletterSerializer

    def get(self, request):
        newsletter = Newsletter.objects.all()
        paginator = PageNumberPagination()

        page_size = 20
        paginator.page_size = page_size        
        page = paginator.paginate_queryset(newsletter, request)

        serializer = NewsletterSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

   
    def post(self, request):
        payload = json.loads(request.body)
        serializer = NewsletterSerializer(data=payload)
        serializer.is_valid(raise_exception=True)
        response = {
            'body': {
                'error':'Unauthorized action'
            },
            'status': status.HTTP_403_FORBIDDEN
        }
        try:
            newsletter = Newsletter.objects.create(
                email=payload['email'],
            )
            response['body'] = NewsletterSerializer(newsletter).data
            response['status'] = status.HTTP_201_CREATED
        except ObjectDoesNotExist as e:
            response['body'] = {'error': str(e)}
            response['status'] = status.HTTP_404_NOT_FOUND
           

        return JsonResponse(response['body'], status=response['status'], safe=False)
