from django.urls.base import reverse
from ..models import Store
from users.models import User
from django.test import TestCase
import uuid

class StoreTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='laye', email='abdoulaye.ndao@xegit.com', password='Passer123')
        self.user.save()
        self.store = Store(name = "Shop",
                            created_by = self.user,
                            store_address = "Lorem ipsum ",
                            is_active = "True"
                        )
        self.store.save()

    def tearDown(self):
        self.user.delete()

    def test_read_store(self):
        self.assertEqual(self.store.name, 'Shop')
        self.assertEqual(self.store.created_by, self.user)
        self.assertEqual(self.store.store_address, 'Lorem ipsum ')
        self.assertEqual(self.store.is_active, 'True')

    def test_update_store_address(self):
        self.store.store_address = 'new store_address'
        self.store.save()
        self.assertEqual(self.store.store_address, 'new store_address')

    
    def test_update_store_is_active(self):
        self.store.is_active = 'False'
        self.store.save()
        self.assertEqual(self.store.is_active, 'False')


    # def test_no_stores(self):
    #     response = self.client.get(reverse('stores'), format='json')
    #     self.assertEqual(response.data, {'stores': []})