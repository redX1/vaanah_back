from django.urls import path

from . import views

urlpatterns = [
    path('orders/initiate', views.InitiateOrderApiView.as_view()),
    path('orders/customers', views.GetCustomerOrderAPIView.as_view()),
    path('orders/sellers', views.GetSellerOrderAPIView.as_view()),
]
