import random
import string
from django.core.mail import EmailMessage
from rest_framework import pagination

DEFAULT_CHAR_STRING = string.ascii_lowercase + string.digits

def generate_random_string(chars=DEFAULT_CHAR_STRING, size=6):
    return ''.join(random.choice(chars) for _ in range(size))

def send_email(data):
    email = EmailMessage(
        subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
    email.content_subtype = "html" 
    email.send()

class CustomPagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        return {
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        }