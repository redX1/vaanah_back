from django.urls import path
from . import views

urlpatterns = [
  path('stores', views.StoreAPIView.as_view()),
  path('stores/', views.StoreSearchAPIView.as_view()),
  path('stores/<uuid:store_id>', views.RetrieveDeleteUpdateStoreAPIView.as_view()),
  path('stores/<uuid:store_id>/products', views.StoreProductsAPIView.as_view()),
  path('stores/activated', views.StoreActivatedAPIView.as_view()),
  path('stores/deactivated', views.StoreDeactivatedAPIView.as_view()),
  path('stores/latest', views.LatestStoreAPIView.as_view()),
]
