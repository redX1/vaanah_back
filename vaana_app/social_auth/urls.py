from . import views
from django.urls import path


urlpatterns = [
    path('social_auth/google/', views.GoogleSocialAuthView.as_view()),
    path('social_auth/facebook/', views.FacebookSocialAuthView.as_view()),

]