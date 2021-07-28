from django.urls import path

from . import views

urlpatterns = [
    path('wallets', views.WalletAPIView.as_view())
]