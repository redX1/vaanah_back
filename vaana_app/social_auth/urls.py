from . import views
from django.urls import path


urlpatterns = [
    path('google/', views.GoogleSocialAuthView.as_view()),
    path('facebook/', views.FacebookSocialAuthView.as_view()),

]