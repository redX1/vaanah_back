from django.test import TestCase
import uuid
from .models import Newsletter
from django.test import TestCase
class NewsletterModelTest(TestCase):
    def setUp(cls):
        cls.newsletter = Newsletter.objects.create(
            email = "test@test.com",
        )

    def test_read_newsletter(self):
        self.assertEqual(self.newsletter.email, "test@test.com")
