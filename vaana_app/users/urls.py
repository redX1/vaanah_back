from django.conf.urls import url
from django.urls import path

from . import views

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    url(r'^users/?$', views.UserRetrieveUpdateAPIView.as_view() ),
    url(r'^users/register/?$', views.RegistrationAPIView.as_view(), name="register"),
    url(r'^users/seller-register/?$', views.SellerRegistrationAPIView.as_view(), name="seller-register"),
    url(r'^users/become-seller/?$', views.BecomeSeller.as_view(), name="seller-register"),
    url(r'^users/login/?$', views.LoginAPIView.as_view(), name="login"),
    path('users/verify/', views.VerifyEmail.as_view(), name="email-verify"),
    path('users/resend/', views.ResendEmailAPI.as_view(), name="email-resend"),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/password/reset/', views.RequestPasswordResetEmail.as_view(), name="request-reset-email"),
    path('users/password/reset/<uidb64>/<token>/', views.PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('users/password/reset/complete/', views.SetNewPasswordAPIView.as_view(), name='password-reset-complete'),
    
    path('users/<int:user_id>/stores', views.UserStoreAPIView.as_view()),
    path('users/all', views.UserAPIView.as_view()),
    path('users/<int:user_id>', views.SingleUserAPIView.as_view()),

]
