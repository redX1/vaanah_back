from django.urls import path

from . import views

urlpatterns = [

    path('newsletter', views.NewsletterAPIView.as_view()),
]
