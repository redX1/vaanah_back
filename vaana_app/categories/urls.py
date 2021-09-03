from os import name
from django.urls import path

from . import views

urlpatterns = [
    path('categories', views.CategoryAPIView.as_view(), name='categories'),
    path('categories/', views.CategorySearchAPIView.as_view()),
    path('categories/<uuid:category_id>', views.CategoryUpdateDeleteAPIView.as_view()),
    path('categories/<uuid:category_id>/products', views.CategoryProductsAPIView.as_view(), name='products-category'),
    path('categories/latest', views.LatestCategoryAPIView.as_view()),
    path('categories/most-viewed', views.MostViewedCategoryAPIView.as_view()),

]
