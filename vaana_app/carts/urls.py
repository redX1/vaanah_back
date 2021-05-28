from django.urls import path

from . import views

urlpatterns = [
    path('carts', views.CartAddView.as_view()),
    path('carts/items/<uuid:id>', views.CartItemUpdateView.as_view()),
    path('carts/items', views.CartItemView.as_view())
]