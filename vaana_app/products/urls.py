from django.urls import path

from . import views

urlpatterns = [

    path('products', views.ProductAPIView.as_view()),
    path('products/<uuid:product_id>', views.RetrieveDeleteUpdateProductAPIView.as_view()),
    path('products/<uuid:product_id>/reviews', views.ProductReviewsAPIView.as_view()),
    path('products/activated', views.ProductActivatedAPIView.as_view()),
    path('products/deactivated', views.ProductDeactivatedAPIView.as_view()),
    path('products/latest', views.LatestProductAPIView.as_view()),

    path('reviews', views.ReviewAPIView.as_view()),
    path('reviews/<uuid:review_id>', views.RetrieveDeleteUpdateReviewAPIView.as_view()),

]
