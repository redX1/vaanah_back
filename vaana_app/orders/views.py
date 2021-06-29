from rest_framework import serializers
from rest_framework.serializers import Serializer
from shippings.models import ShippingMethod
from addresses.models import Address
from carts.models import Cart
from .models import Order, ShippingAddress
from .serializers import OrderSerializer, SellerOrderSerializer, ShippingAddressSerializer
from shippings.serializers import ShippingMethodSerializer
from products.serializers import ProductSerializer
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
            cart = Cart.objects.get(id=data['cart'], status=Cart.OPEN)
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
            email_data = {'email_body': 'Your order ' + order.number + ' has been initiated, you can pay to confirm your order.', 'to_email': user.email,
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

class GetCustomerOrderAPIView(APIView):
    @csrf_exempt
    @permission_classes([IsAuthenticated])
    def get(self, request, *args, **kwargs):
        user = request.user

        orders = Order.objects.filter(user=user)
        serializer = OrderSerializer(orders, many=True)

        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)

class GetSellerOrderAPIView(APIView):

    def getSellerOrder(self, order, products):
        return {
            'id': order.id,
            'number': order.number,
            'products': ProductSerializer(products, many=True).data,
            "currency": order.currency,
            "total_tax": order.total_tax,
            "shipping_tax": order.shipping_tax,
            "total_prices": order.total_prices,
            "shipping_address": ShippingAddressSerializer(order.shipping_address).data,
            "shipping_method": ShippingMethodSerializer(order.shipping_method).data,
            "status": order.status,
            "created_at": order.created_at,
            "updated_at": order.updated_at,
        }

    def filterOrderBySeller(self, order, user):
        products = []
        cart = order.cart

        for item in cart.items.all():
            product = item.product
            if product.created_by.email == user.email:
                products.append(product)
        return None if len(products) == 0 else self.getSellerOrder(order, products)

    @csrf_exempt
    @permission_classes([IsAuthenticated])
    def get(self, request, *args, **kwargs):
        user = request.user

        response = {
            'body': {
                'error': 'Unauthorized action'
            },
            'status': status.HTTP_401_UNAUTHORIZED
        }

        if user.account_type == 'Seller':
            orders = Order.objects.filter(status=Order.CONFIRMED)
            data = []
            for order in orders:
                f_order = self.filterOrderBySeller(order, user)
                if f_order is not None:
                    data.append(f_order)
            response['body'] = data
            response['status'] = status.HTTP_200_OK

        return JsonResponse(response['body'], status=response['status'], safe=False)