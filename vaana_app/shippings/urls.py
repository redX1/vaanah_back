from django.urls import path

from . import views

urlpatterns = [

    path('carriers', views.ShippoCarrierAPIVIew.as_view()),
    path('shipments', views.ShippoShipmentAPIView.as_view()),

]
