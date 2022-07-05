from rest_framework.test import APISimpleTestCase
from django.urls import reverse, resolve

from accounts.views import UserRegistrationView, UserLoginView, ChangePasswordView, SendResetPasswordEmailView, \
    ResetPasswordView, UserProfileView


class TestUrls(APISimpleTestCase):
    """
    class to test all the urls of accounts app
    """


    def check_urls(self, url, view):
        """
        function to test if the given url matches with its view
        :param url: url to be tested
        :type url: str
        :param view: view connected to the url
        """
        self.assertEqual(resolve(url).func.view_class, view)

    def test_registration_url(self):
        """
        function to test if the registration url works
        """
        self.check_urls(reverse('register'), UserRegistrationView)

    def test_login_url(self):
        """
        function to test if the login url works
        """
        self.check_urls(reverse('login'), UserLoginView)

    def test_change_password_url(self):
        """
        function to test if the login url works
        """
        self.check_urls(reverse('change_password'), ChangePasswordView)

    def test_send_reset_password_email_url(self):
        """
        function to test if the url that sends the reset password email works
        """
        self.check_urls(reverse('send_reset_password_email'), SendResetPasswordEmailView)

    def test_reset_password_url(self):
        """
        function to test if the reset password url works
        """
        self.check_urls(reverse('reset_password', kwargs={'user_id': 1, 'token': 'random_token'}), ResetPasswordView)

    def test_profile_url(self):
        """
        function to test if the user profile url works
        """
        self.check_urls(reverse('profile'), UserProfileView)
