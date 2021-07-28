from categories.models import Category
import uuid
from users.models import User
from django.conf import settings
from ..models import Store
from django.test import TestCase

class StoreModelTest(TestCase):
    def setUp(cls):
        cls.store = Store.objects.create(
            id = uuid.uuid4,
            name = "Foods",
            address = "Lorem ipsum dolor, sit amet consectetur adipisicing elit.",
            is_active = "True",
            created_by = User.objects.create(username='user5', email='email5@im.com', password='test')
        )

    # def test_wrong_store_fields(self):

    #     store = Store.objects.create(
    #         id = "",
    #         name = "Foods",
    #         address = "Lorem ipsum dolor, sit amet consectetur adipisicing elit.",
    #         is_active = "True",
    #         created_by = self.store.created_by
    #     )
    #     store.save()
    #     self.assertEqual(store.status_code, 200)