from django.urls import path

from . import views

urlpatterns = [
    path('', views.CategoryAPIView.as_view()),
    # path('', views.CreateCategoryAPIView.as_view()),
    path('<int:category_id>', views.UpdateCategoryAPIView.as_view()),
    path('<int:category_id>', views.DeleteCategoryAPIView.as_view()),

]
