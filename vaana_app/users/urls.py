from django.conf.urls import url
from django.urls import path

from .views import (
    LoginAPIView, LogoutAPIView, PasswordTokenCheckAPI, RegistrationAPIView, RequestPasswordResetEmail, SetNewPasswordAPIView, UserRetrieveUpdateAPIView, VerifyEmail
)
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    url(r'^users/?$', UserRetrieveUpdateAPIView.as_view()),
    url(r'^users/register/?$', RegistrationAPIView.as_view()),
    url(r'^users/login/?$', LoginAPIView.as_view()),

    path('users/verify/', VerifyEmail.as_view(), name="email-verify"),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/reset/email/', RequestPasswordResetEmail.as_view(), name="request-reset-email"),
    path('users/password/reset/<uidb64>/<token>/', PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('users/password/reset/complete/', SetNewPasswordAPIView.as_view(), name='password-reset-complete'),
    
]
