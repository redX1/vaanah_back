from django.conf.urls import url

from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView, VerifyEmail
)
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    url(r'^users/?$', UserRetrieveUpdateAPIView.as_view()),
    url(r'^users/register/?$', RegistrationAPIView.as_view()),
    url(r'^users/login/?$', LoginAPIView.as_view()),

    url(r'^email-verify/', VerifyEmail.as_view(), name="email-verify"),

    url(r'^token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
]
