from django.urls import path
from . import views

urlpatterns = [
 
  path('wishlist', views.WishListAddView.as_view()),
  path('wishlist/items/<uuid:id>', views.WishListItemUpdateView.as_view()),
  path('wishlist/items', views.WishListItemView.as_view())
]
