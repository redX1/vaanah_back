from django.urls import path

from . import views

urlpatterns = [
    path('categories', views.CategoryAPIView.as_view()),
    path('categories/<int:category_id>', views.CategoryDetailAPIView.as_view()),
    path('categories/<int:category_id>', views.UpdateCategoryAPIView.as_view()),
    path('categories/<int:category_id>', views.DeleteCategoryAPIView.as_view()),

]
