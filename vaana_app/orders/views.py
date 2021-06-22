from shippings.models import ShippingMethod
from addresses.models import Address
from carts.models import Cart
from .models import Order, ShippingAddress
from .serializers import OrderSerializer
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
from rest_framework.decorators import api_view, permission_classes
from cores.utils import *

class InitiateOrderApiView(APIView):
    @csrf_exempt
    @permission_classes([IsAuthenticated])
    def post(self, request, *args, **kwargs):
        user = request.user
        payload = json.loads(request.body)
        serializer = OrderSerializer(data=payload)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        number = Util.getOrderNumber()
        shipping_address_data = data['shipping_address']
        address_data =shipping_address_data['address']
        shipping_method_data = data['shipping_method']

        try:
            cart = Cart.objects.get(id=data['cart'])
            address = Address.objects.create(country=address_data["country"], state=address_data['state'], street=address_data['street'], zipcode=address_data['zipcode'])
            shipping_address = ShippingAddress.objects.create(address=address, phone_number=shipping_address_data['phone_number'], notes=shipping_address_data['notes'])
            shipping_method = ShippingMethod.objects.create(name=shipping_method_data['name'], price=shipping_method_data['price'], currency=shipping_method_data['currency'])
            order = Order.objects.create(
                number=number, 
                user=user, 
                cart=cart, 
                currency=data['currency'], 
                shipping_address=shipping_address,
                total_tax=data['total_tax'],
                shipping_tax=data['shipping_tax'],
                total_prices=data['total_prices'],
                shipping_method=shipping_method
                )
            cart.status = Cart.SUBMITTED
            cart.save()
            email_data = {'email_body': 'Your order ' + order.number + ' has initiated, you can pay to confirm your order.', 'to_email': user.email,
                'email_subject': 'Order initiated'}
            send_email(email_data)
            response = {
                'body': OrderSerializer(order).data,
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