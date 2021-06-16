from os import name
from django.urls import path

from . import views

urlpatterns = [
    path('categories', views.CategoryAPIView.as_view(), name='categories'),
    path('categories/<uuid:category_id>', views.RetrieveDeleteUpdateCategoryAPIView.as_view()),
    path('categories/<uuid:category_id>/products', views.CategoryProductsAPIView.as_view(), name='products-category'),
    path('categories/activated', views.CategoryActivatedAPIView.as_view()),
    path('categories/deactivated', views.CategoryDeactivatedAPIView.as_view()),
    path('categories/latest', views.LatestCategoryAPIView.as_view()),

]
