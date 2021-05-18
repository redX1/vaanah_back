from django.urls import path

from . import views

urlpatterns = [

    path('products', views.ProductAPIView.as_view()),
    path('products/<int:product_id>', views.ProductDetailAPIView.as_view()),
    path('products/<int:product_id>', views.UpdateProductAPIView.as_view()),
    path('products/<int:product_id>', views.DeleteProductAPIView.as_view()),
]
