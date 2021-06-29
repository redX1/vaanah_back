from categories.models import Category
import uuid
from users.models import User
from django.conf import settings
from ..models import Product
from django.test import TestCase

class ProductModelTest(TestCase):
    def setUp(cls):
        cls.product = Product.objects.create(
            id = uuid.uuid4,
            name = "Foods",
            slug = "foods",
            description = "Lorem ipsum dolor, sit amet consectetur adipisicing elit.",
            is_active = "True",
            created_by = User.objects.create(username='user1', email='email1@im.com', password='test'),
            price = "200",
            category = Category.objects.create(
                id = uuid.uuid4,
                name = "Foods",
                slug = "foods",
                description = "Lorem ipsum dolor, sit amet consectetur adipisicing elit.",
                is_active = "True",
                created_by = User.objects.create(username='user0', email='email0@im.com', password='test')
            ),
            # store = "",
            image = "test",
            quantity ="50"
        )

    # def test_wrong_product_fields(self):

    #     product = Product.objects.create(
    #         id = "",
    #         name = "Foods",
    #         slug = "foods",
    #         description = "Lorem ipsum dolor, sit amet consectetur adipisicing elit.",
    #         is_active = "True",
    #         created_by = self.product.created_by
    #     )
    #     product.save()
    #     self.assertEqual(product.status_code, 200)