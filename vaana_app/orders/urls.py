from django.urls import path

from . import views

urlpatterns = [
    path('orders', views.OrderApiView.as_view()),
]
