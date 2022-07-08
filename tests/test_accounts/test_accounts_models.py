from rest_framework.test import APITestCase

from accounts.models import User


class TestModels(APITestCase):
    """
    class to test models of accounts app
    """

    def setUp(self):
        self.email = 'test@gmail.com'
        self.username = 'test_user'
        self.first_name = 'test'

        self.last_name = 'test'
        self.contact_number = '+919876543210'

        self.create_user = User.objects.create(email=self.email, username=self.username, first_name=self.first_name,
                                               last_name=self.last_name, contact_number=self.contact_number,
                                               is_event_manager=True)

    def test_user_model(self):
        """
        function to test if the user model functions correctly
        """
        self.assertEqual(self.create_user.email, self.email)
        self.assertEqual(self.create_user.username, self.username)
        self.assertEqual(self.create_user.first_name, self.first_name)
        self.assertEqual(self.create_user.last_name, self.last_name)
        self.assertEqual(self.create_user.contact_number, self.contact_number)
