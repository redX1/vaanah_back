from .models import Email
from rest_framework import serializers
from django.core.mail import send_mail

class EmailVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = [
            'email',
            "mail_to",
            "subject",
            "body",
        ]

    # def create(self, validate_data):
    #     instance = super(EmailVerificationSerializer, self).create(validate_data)
    #     send_mail(
    #         'Instance {} has been created'.format(instance.pk),
    #         'Here is the message. DATA: {}'.format(validate_data),
    #         'from@example.com',
    #         ['to@example.com'],
    #         fail_silently=False,
    #     )
    #     return instance

