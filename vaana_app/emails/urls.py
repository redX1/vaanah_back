from django.urls import path

from .views import (
    RequestPasswordResetEmail, EmailAPIView
)

urlpatterns = [

    path('emails/verify', EmailAPIView.as_view()),
    path('emails/password/reset/', RequestPasswordResetEmail.as_view(), name="request-reset-email"),
]
