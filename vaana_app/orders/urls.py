from django.urls import path

from . import views

urlpatterns = [
    path('orders/initiate', views.InitiateOrderApiView.as_view()),
    path('orders', views.GetOrdersAPIView.as_view()),
]
