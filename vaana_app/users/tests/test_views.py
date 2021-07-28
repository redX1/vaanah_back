import pdb
from .test_setup import TestSetUp
from ..models import User
class TestViews(TestSetUp):
    def test_user_cannot_register_with_no_data(self):
        res=self.client.post(self.register_url)
        self.assertEqual(res.status_code, 400)

    def test_user_can_register_correctly(self):
        res=self.client.post(self.register_url, self.user_data, format="json")
        # self.assertEqual(res.data, self.user_data)
        self.assertEqual(res.status_code, 201)

    def test_user_cannot_login_with_unverified_email(self):
        self.client.post(self.register_url, self.user_data, format="json")
        res=self.client.post(self.login_url, self.user_data, format="json")
        
        self.assertEqual(res.status_code, 400)

    def test_user_can_login_after_verification(self):
        email = 'fatma.lo@terinnova.com'
        response=self.client.post(self.register_url, self.user_data, format="json")
        user=User.objects.get(email=email)
        user.is_verified = True
        user.save()
        res=self.client.post(self.login_url, self.user_data, format="json")
        
        self.assertEqual(response.data['email'], self.user_data['email'])
        self.assertEqual(res.status_code, 200)
