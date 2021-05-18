from django.urls import path

from . import views

urlpatterns = [
    path('', views.CategoryAPIView.as_view()),
    path('update/<int:category_id>', views.UpdateCategoryAPIView.as_view()),
    path('delete/<int:category_id>', views.DeleteCategoryAPIView.as_view()),

]
