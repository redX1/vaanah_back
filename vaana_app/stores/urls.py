from django.urls import path
from . import views

urlpatterns = [
  path('stores', views.StoreAPIView.as_view()),
  path('stores/<int:store_id>', views.StoreDetailAPIView.as_view()),
  path('stores/<int:store_id>', views.UpdateStoreAPIView.as_view()),
  path('stores/<int:store_id>', views.DeleteStoreAPIView.as_view()),
  path('stores/<int:store_id>/products', views.StoreProductsAPIView.as_view())

]
