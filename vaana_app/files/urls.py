from django.urls import path

from . import views

urlpatterns = [
    path('files', views.FileUploadAPIView.as_view()),
]