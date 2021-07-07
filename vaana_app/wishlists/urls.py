from django.urls import path
from . import views

urlpatterns = [
 
  path('wishlists', views.WishListAddView.as_view()),
  path('wishlists/items/<uuid:id>', views.WishListItemUpdateView.as_view()),
  path('wishlists/items', views.WishListItemView.as_view())
]
