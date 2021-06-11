from django.shortcuts import render

from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.http import HttpResponseRedirect
from rest_framework.views import APIView
import json
import jwt
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .serializers import (
     ResetPasswordEmailRequestSerializer
)

class EmailAPIView(APIView, SuccessMessageMixin, CreateView):

    def post(self, request):
        user = json.loads(request.body)

        # The create serializer, validate serializer, save serializer pattern
        # below is common and you will see it a lot throughout this course and
        # your own work later on. Get familiar with it.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        subject = ''
        message = ''
        recepient = ''
        data = {'email_body': message, 'to_email': recepient, 'email_subject': subject}

        Util.send_email(data)

        return Response("Successfully sent", status=status.HTTP_201_CREATED)

class RequestPasswordResetEmail(APIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data.get('email', '')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request=request).domain
            relativeLink = reverse('password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})

            redirect_url = request.data.get('redirect_url', '')
            absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
            subject = 'Password reset'
            message = 'Hi '+user.username + ''  + absurl+"?redirect_url="+redirect_url
            recepient = user.email
            data = {'email_body': message, 'to_email': recepient, 'email_subject': subject}
            Util.send_email(data)
        return Response({'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)


