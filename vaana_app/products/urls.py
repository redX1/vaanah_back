from django.urls import path

from . import views

urlpatterns = [

    path('products', views.ProductAPIView.as_view()),
    path('products/<int:product_id>', views.RetrieveDeleteUpdateProductAPIView.as_view()),
    path('reviews', views.ReviewAPIView.as_view()),
    path('reviews/<int:review_id>', views.RetrieveDeleteUpdateReviewAPIView.as_view()),

]
