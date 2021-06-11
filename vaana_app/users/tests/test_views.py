from .test_setup import TestSetUp

class TestViews(TestSetUp):
    def test_user_can_register_with_no_data(self):
        res=self.client.post(self.register_url)
        self.assertEquall(res.status_code, 400)

