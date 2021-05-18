from django.urls import path
from . import views

urlpatterns = [
  path('stores', views.StoreAPIView.as_view()),
  path('stores/<int:store_id>', views.RetrieveDeleteUpdateStoreAPIView.as_view()),
  path('stores/<int:store_id>/products', views.StoreProductsAPIView.as_view())


]
