from django.urls import path

from . import views

urlpatterns = [

    path('products', views.ProductAPIView.as_view()),
    path('products/', views.ProductSearchAPIView.as_view()),
    path('products/<uuid:product_id>', views.ProductUpdateDeleteAPIView.as_view()),
    path('products/<uuid:product_id>/reviews', views.ProductReviewsAPIView.as_view()),
    path('products/latest', views.LatestProductAPIView.as_view()),
    path('products/most-viewed', views.MostViewedProductAPIView.as_view()),

    path('products/reviews', views.ProductReviewsAPIView.as_view()),
    path('products/reviews/<uuid:review_id>', views.ProductReviewUpdateDeleteAPIView.as_view()),
    path('products/sellers', views.SellerProductAPIView.as_view()),

]
