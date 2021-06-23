from .models import PaymentModel
from django.core.exceptions import ObjectDoesNotExist
from stripe.api_resources import line_item
from orders.models import Order
from orders.serializers import OrderSerializer
from .serializers import PaymentSerializer, StripePaymentIntentConfirmSerializer
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import serializers, status
import json
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView
import stripe
from django.conf import settings
from cores.utils import *
from carts.models import Cart
from products.models import Product

stripe.api_key = settings.STRIPE_SECRET_KEY

def updateProductsQuantity(cart):
    
    for item in cart.items.all():
        try:
            product = item.product
            product.quantity = product.quantity - item.quantity
            product.save()
        except Exception as e:
            pass

class InitiateStripePayement(APIView):
    @csrf_exempt
    @permission_classes([IsAuthenticated])
    def post(self, request, *args, **kwargs):
        user = request.user
        payload = json.loads(request.body)
        serializer = PaymentSerializer(data=payload)
        serializer.is_valid(raise_exception=True)

        try:
            customer = stripe.Customer.create(
                name=user.username,
                email=user.email
            )
            intent = stripe.PaymentIntent.create(
                payment_method_types=['card'],
                amount = payload['amount'] * 100,
                currency = 'EUR',
                customer=customer.id
            )
            serializer.save()
            response = {
                'body': {
                    'token': intent['client_secret'],
                    'public_key': settings.STRIPE_PUBLISHABLE_KEY,
                    'payment': serializer.data
                },
                'status': status.HTTP_200_OK
            }
        except Exception as e:
            response = {
                'body': {
                    'error': str(e)
                },
                'status': status.HTTP_403_FORBIDDEN            
            }
        return JsonResponse(response['body'], status = response['status'], safe=False)

class ConfirmStripePayment(RetrieveUpdateAPIView):
    @csrf_exempt
    @permission_classes([IsAuthenticated])
    def update(self, request,payment_intent_id):
        user = request.user
        payload = json.loads(request.body)
        serializer = StripePaymentIntentConfirmSerializer(data=payload)
        serializer.is_valid(raise_exception=True)

        try:
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            response = {
                'body': {
                    'error': 'Intent not valid'
                },
                'status': status.HTTP_400_BAD_REQUEST            
            }

            if intent['status'] == 'succeeded':
                try:
                    order = Order.objects.get(number=payload['order_number'], user=user)
                    payment = PaymentModel.objects.get(order_number=payload['order_number'])
                    order.status = Order.CONFIRMED
                    order.save()
                    payment.status = PaymentModel.DONE
                    payment.save()
                    email_data = {'email_body': 'Your order ' + order.number + ' has been confirmed.', 'to_email': user.email,
                'email_subject': 'Order confirmed'}
                    send_email(email_data)
                    updateProductsQuantity(order.cart)
                    response['body'] = OrderSerializer(order).data
                    response['status'] = status.HTTP_200_OK
                except ObjectDoesNotExist:
                    response['body']['error']= 'Order or payment not founded'
                    response['status'] = status.HTTP_400_BAD_REQUEST

        except Exception as e:
            response = {
                'body': {
                    'error': str(e)
                },
                'status': status.HTTP_403_FORBIDDEN            
            }
        return JsonResponse(response['body'], status = response['status'], safe=False)
