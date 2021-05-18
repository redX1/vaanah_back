from django.urls import path

from . import views

urlpatterns = [
    path('categories', views.CategoryAPIView.as_view()),
    path('categories/<int:category_id>', views.RetrieveDeleteUpdateCategoryAPIView.as_view())
]
