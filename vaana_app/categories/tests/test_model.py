import uuid
from users.models import User
from django.conf import settings
from django.forms.fields import SlugField, UUIDField
from ..models import Category
from django.test import TestCase

class CategoryModelTest(TestCase):
    def setUp(cls):
        cls.category = Category.objects.create(
            id = uuid.uuid4,
            name = "Foods",
            slug = "foods",
            description = "Lorem ipsum dolor, sit amet consectetur adipisicing elit.",
            is_active = "True",
            created_by = User.objects.create(username='user', email='email@im.com', password='test')
        )

    # def test_wrong_category_fields(self):

    #     category = Category.objects.create(
    #         id = "",
    #         name = "Foods",
    #         slug = "foods",
    #         description = "Lorem ipsum dolor, sit amet consectetur adipisicing elit.",
    #         is_active = "True",
    #         created_by = self.category.created_by
    #     )
    #     category.save()
    #     self.assertEqual(category.status_code, 200)
