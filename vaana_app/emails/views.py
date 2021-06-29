
from .serializers import EmailVerificationSerializer
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
import json
from .utils import Util
from rest_framework import status
from rest_framework.response import Response
from django.core.mail import send_mail

class EmailAPIView(CreateAPIView):
    serializer_class = EmailVerificationSerializer

    def post(self, request):
        serializer = EmailVerificationSerializer(request.data)
        # if serializer.is_valid():
        #     data = serializer.validated_data
        #     email = data.get('email')
        #     subject = data.get('subject')
        #     send_mail(
        #         'Sent email from {}'.format(subject),
        #         'Here is the message. {}'.format(validated_data.get('message')),
        #         email,
        #         ['to@example.com'],
        #         fail_silently=False,
        #     )
        #     return Response({"success": "Sent"}, status=status.HTTP_201_CREATED)
        # return Response({'error': "Failed"}, status=status.HTTP_400_BAD_REQUEST)

        # user = json.loads(request.body)
        # serializer = self.serializer_class(data=user)
        # serializer.is_valid(raise_exception=True)
        # serializer.save()
        # print(user)

        subject = 'test'
        email = 'test'
        mail_to = 'fatma.lo@xegit.com'
        data = {'email_body': email, 'to_email': mail_to, 'email_subject': subject}

        Util.send_email(data)

        return Response("Successfully sent", status=status.HTTP_201_CREATED)



