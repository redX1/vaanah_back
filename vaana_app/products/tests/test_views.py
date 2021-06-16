from django.urls.base import reverse
from ..models import Product
from users.models import User
from categories.models import Category
from django.test import TestCase
import uuid

class ProductTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='user', email='email@im.com', password='test')
        self.user.save()
        self.product = Product.objects.create(
            id = uuid.uuid4,
            name = "Foods",
            slug = "foods",
            description = "Lorem ipsum dolor, sit amet consectetur adipisicing elit.",
            is_active = "True",
            created_by = User.objects.create(username='user', email='email@im.com', password='test'),
            price = "200",
            category = Product.objects.create(
                id = uuid.uuid4,
                name = "Foods",
                slug = "foods",
                description = "Lorem ipsum dolor, sit amet consectetur adipisicing elit.",
                is_active = "True",
                created_by = User.objects.create(username='user', email='email@im.com', password='test')
            ),
            # store = "",
            image = "test",
            quantity ="50"
        )
        self.product.save()

    def tearDown(self):
        self.user.delete()

    def test_read_product(self):
        self.assertEqual(self.product.created_by, self.user)
        self.assertEqual(self.product.name, 'Foods')
        self.assertEqual(self.product.description, 'Lorem ipsum dolor, sit amet consectetur adipisicing elit.')
        self.assertEqual(self.product.slug, 'foods')
        self.assertEqual(self.product.is_active, 'True')

    def test_update_product_description(self):
        self.product.description = 'new description'
        self.product.save()
        self.assertEqual(self.product.description, 'new description')

    
    def test_update_product_name(self):
        self.product.name = 'new name'
        self.product.save()
        self.assertEqual(self.category.name, 'new name')


    # def test_no_products(self):
    #     response = self.client.get(reverse('products'), format='json')
    #     self.assertEqual(response.data, {'products': []})