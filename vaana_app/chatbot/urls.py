from os import name
from django.urls import path

from . import views

urlpatterns = [ 
    path('chatbot', views.ChatterBotAPIView.as_view(), name='chatbot'),
]