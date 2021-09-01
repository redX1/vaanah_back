from django.test.testcases import SimpleTestCase
from django.urls.base import reverse
from ..models import Category
from users.models import User
from products.models import Product
from django.test import TestCase

class CategorySimpleTest(SimpleTestCase):
    def test_url_status(self):
        response = self.client.get('categories')
        self.assertEquals(response.status_code, 404)

class CategoryTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='laye', email='abdoulaye.ndao@xegit.com', password='Passer123')
        self.user.save()
        self.category = Category(name = "Foods",
                                    slug = "foods",
                                    description = "Lorem ipsum dolor, sit amet consectetur adipisicing elit.",
                                    is_active = "True",
                                    created_by = self.user
                        )
        self.category.save()

    def tearDown(self):
        self.user.delete()

    def test_read_category(self):
        self.assertEqual(self.category.created_by, self.user)
        self.assertEqual(self.category.name, 'Foods')
        self.assertEqual(self.category.description, 'Lorem ipsum dolor, sit amet consectetur adipisicing elit.')
        self.assertEqual(self.category.slug, 'foods')
        self.assertEqual(self.category.is_active, 'True')

    def test_update_category_description(self):
        self.category.description = 'new description'
        self.category.save()
        self.assertEqual(self.category.description, 'new description')

    
    def test_update_category_name(self):
        self.category.name = 'new name'
        self.category.save()
        self.assertEqual(self.category.name, 'new name')


    # def test_no_categories(self):
    #     response = self.client.get(reverse('categories'), format='json')
    #     self.assertEqual(response.data, {'categories': []})

