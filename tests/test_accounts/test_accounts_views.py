from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework.test import APITestCase

from accounts.models import User


class TestViews(APITestCase):
    """
    class to test views of accounts app
    """

    def setUp(self):

        self.create_user = User.objects.create_user(email='test@gmail.com', username='test', first_name='heli',
                                                    last_name='shah', password='Abc@1234',
                                                    contact_number='+919876543210', is_event_manager=True)

        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.change_password_url = reverse('change_password')
        self.send_reset_password_email_url = reverse('send_reset_password_email')
        self.profile_url = reverse('profile')

    def register_user_data(self, email, username, first_name, last_name, contact_number, password, password2):
        """
        to create user data
        """
        self.user_registration_data = {
            'email': email,
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
            'contact_number': contact_number,
            'password': password,
            'password2': password2,
        }
        return self.user_registration_data

    def test_cannot_register_with_no_data(self):
        """
        function to test that registration is not successful with no data
        """
        response = self.client.post(self.register_url)
        self.assertEqual(response.status_code, 400)

    def test_registration_successful(self):
        """
        function to test that registration is successful
        """
        data = self.register_user_data('heli@gmail.com', 'heli', 'shah', 'shah', '+919087654321', 'Abc@1234',
                                       'Abc@1234')

        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, 201)

    def test_cannot_register_without_email(self):
        """
        function to test that registration is not successful without email
        """
        data = self.register_user_data(None, 'heli', 'heli', 'shah', '+919087654321', 'Abc@1234', 'Abc@1234')

        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_cannot_register_with_invalid_email(self):
        """
        function to test that registration is not successful with invalid email
        """
        data = self.register_user_data('heli.com', 'heli', 'heli', 'shah', '+919087654321', 'Abc@1234', 'Abc@1234')

        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_cannot_register_if_email_already_exists(self):
        """
        function to test that registration is not successful if the email is not unique
        """
        data = self.register_user_data('test@gmail.com', 'heli', 'heli', 'shah', '+919087654321', 'Abc@1234',
                                       'Abc@1234')
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_cannot_register_without_username(self):
        """
        function to test that registration is not successful without username
        """
        data = self.register_user_data('heli@gmail.com', None, 'heli', 'shah', '+919087654321', 'Abc@1234', 'Abc@1234')

        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_cannot_register_with_invalid_username(self):
        """
        function to test that registration is not successful with invalid username
        """
        data = self.register_user_data('heli.com', 'Heli 1', 'heli', 'shah', '+919087654321', 'Abc@1234', 'Abc@1234')

        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_cannot_register_if_username_already_exists(self):
        """
        function to test that registration is not successful if the username is not unique
        """
        data = self.register_user_data('heli@gmail.com', 'test', 'heli', 'shah', '+919087654321', 'Abc@1234',
                                       'Abc@1234')
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_cannot_register_without_first_name(self):
        """
        function to test that registration is not successful without first name
        """
        data = self.register_user_data('heli@gmail.com', 'heli', None, 'shah', '+919087654321', 'Abc@1234', 'Abc@1234')

        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_cannot_register_with_invalid_first_name(self):
        """
        function to test that registration is not successful with invalid first name
        """
        data = self.register_user_data('heli.com', 'heli', 'hel i', 'shah', '+919087654321', 'Abc@1234', 'Abc@1234')

        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_cannot_register_without_last_name(self):
        """
        function to test that registration is not successful without last name
        """
        data = self.register_user_data('heli@gmail.com', 'heli', 'heli', None, '+919087654321', 'Abc@1234', 'Abc@1234')

        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_cannot_register_with_invalid_last_name(self):
        """
        function to test that registration is not successful with invalid last name
        """
        data = self.register_user_data('heli.com', 'heli', 'heli', '1shah', '+919087654321', 'Abc@1234', 'Abc@1234')

        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_cannot_register_without_contact_number(self):
        """
        function to test that registration is not successful without contact number
        """
        data = self.register_user_data('heli@gmail.com', 'heli', 'heli', 'shah', None, 'Abc@1234', 'Abc@1234')

        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_cannot_register_with_invalid_contact_number(self):
        """
        function to test that registration is not successful with invalid contact number
        """
        data = self.register_user_data('heli.com', 'heli', 'heli', 'shah', '+914087654321', 'Abc@1234', 'Abc@1234')

        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_cannot_register_if_contact_number_already_exists(self):
        """
        function to test that registration is not successful if the contact_number is not unique
        """
        data = self.register_user_data('heli@gmail.com', 'heli', 'heli', 'shah', '+919876543210', 'Abc@1234',
                                       'Abc@1234')
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_cannot_register_without_password(self):
        """
        function to test that registration is not successful without password
        """
        data = self.register_user_data('heli@gmail.com', 'heli', 'shah', 'shah', '+919087654321', None, 'Abc@1234')

        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_cannot_register_with_invalid_password(self):
        """
        function to test that registration is not successful with invalid password
        """
        data = self.register_user_data('heli.com', 'heli', 'heli', 'shah', '+919087654321', 'Abc1234', 'Abc1234')

        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_cannot_register_without_password2(self):
        """
        function to test that registration is not successful without password2
        """
        data = self.register_user_data('heli@gmail.com', 'heli', 'shah', 'shah', '+919087654321', 'Abc@1234', None)

        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_cannot_register_if_passwords_does_not_match(self):
        """
        function to test that registration is not successful if password and password2 does not match
        """
        data = self.register_user_data('heli.com', 'heli', 'heli', 'shah', '+919087654321', 'Abc@1234', 'Abc1234')

        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_cannot_login_with_no_data(self):
        """
        function to test that login isn't successful without any data
        """
        self.assertFalse(self.client.login(email=None, password=None))

    def test_cannot_login_with_false_email(self):
        """
        function to test that login isn't successful with false email
        """
        self.assertFalse(self.client.login(email='testing@gmail.com', password='Abc@1234'))

    def test_cannot_login_with_false_password(self):
        """
        function to test that login isn't successful false password
        """
        self.assertFalse(self.client.login(email='test@gmail.com', password='abc1234'))

    def test_cannot_login_if_email_and_password_does_not_match(self):
        """
        function to test that login isn't successful if the email and password doesn't match
        """
        self.assertFalse(self.client.login(email='test@gmail.com', password='Abc@134'))

    def test_login_successful(self):
        """
        function to test that login is successful if the email and password are correct
        """
        self.assertTrue(self.client.login(email='test@gmail.com', password='Abc@1234'))

    def test_change_password_does_not_work_if_current_password_is_false(self):
        """
        password cannot be changed if current password is wrong
        """
        user = User.objects.get(username='test')
        self.client.force_authenticate(user=user)
        response = self.client.post(self.change_password_url, {'current_password': 'abc12345', 'password': 'Abc@12345',
                                                               'password2': 'Abc@12345'})
        self.assertEqual(response.status_code, 400)

    def test_change_password_does_not_work_if_passwords_does_not_match(self):
        """
        password cannot be changed if password and password2 does not match
        """
        user = User.objects.get(username='test')
        self.client.force_authenticate(user=user)
        response = self.client.post(self.change_password_url, {'current_password': 'Abc@1234', 'password': 'Abc@12345',
                                                               'password2': 'Abc@1245'})
        self.assertEqual(response.status_code, 400)

    def test_change_password_successful(self):
        """
        password can be changed if all the data is valid
        """
        user = User.objects.get(username='test')
        self.client.force_authenticate(user=user)
        response = self.client.post(self.change_password_url, {'current_password': 'Abc@1234', 'password': 'Abc@12345',
                                                               'password2': 'Abc@12345'})
        self.assertEqual(response.status_code, 200)

    def test_send_reset_password_email_fails_if_wrong_email(self):
        """
        password reset email is not sent if the email is wrong or not registered in the database
        """
        user = User.objects.get(username='test')
        self.client.force_authenticate(user=user)
        response = self.client.post(self.send_reset_password_email_url, {'email': 'testing@gmail.com'})
        self.assertEqual(response.status_code, 400)

    def test_send_reset_password_email_successful(self):
        """
        password reset email is not sent if the data is valid
        """
        user = User.objects.get(username='test')
        self.client.force_authenticate(user=user)
        response = self.client.post(self.send_reset_password_email_url, {'email': 'test@gmail.com'})
        self.assertEqual(response.status_code, 200)

    def test_reset_password_fails_if_passwords_does_not_match(self):
        """
        password cannot be reset if password and password2 does not match
        """
        user = User.objects.get(username='test')
        self.client.force_authenticate(user=user)
        url = reverse('reset_password', kwargs={'user_id': user.id, 'token': 'random_token'})
        response = self.client.post(url, {'password': 'Abc@1234', 'password2': 'Abc@123'})
        self.assertEqual(response.status_code, 400)

    def test_reset_password_successful(self):
        """
        password can be reset if password and password2 are valid and matches
        """
        user = User.objects.get(username='test')
        self.client.force_authenticate(user=user)
        user_id = urlsafe_base64_encode(force_bytes(user.id))
        token = PasswordResetTokenGenerator().make_token(user)
        url = reverse('reset_password', kwargs={'user_id': user_id, 'token': token})
        response = self.client.post(url, {'password': 'Abc@1234', 'password2': 'Abc@1234'})
        self.assertEqual(response.status_code, 200)

    def test_access_profile_fails_if_user_is_unauthenticated(self):
        """
        user cannot access his/her profile if not authenticated
        """
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 401)

    def test_get_profile_successfully(self):
        """
        user can get/view his/her profile
        """
        user = User.objects.get(username='test')
        self.client.force_authenticate(user=user)
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)

    def update_profile(self, field, value):
        """
        function for update profile

        :param field: field_name of the model to be updated
        :param value: value of the field that is passed
        :return: response of the 'put' testing
        """
        user = User.objects.get(username='test')
        self.client.force_authenticate(user=user)

        data = {
            field: value
        }

        return self.client.put(self.profile_url, data)

    def test_update_profile_fails_if_data_is_invalid(self):
        """
        update profile fails if the data entered is not valid or not unique
        """
        invalid_email_response = self.update_profile('email', 'heli.com')
        self.assertEqual(invalid_email_response.status_code, 400)

        invalid_contact_number_response = self.update_profile('contact_number', '+9112345678')
        self.assertEqual(invalid_contact_number_response.status_code, 400)

    def test_update_profile_successful(self):
        """
        profile can be updated successfully if valid data is passed
        """
        first_name_response = self.update_profile('first_name', 'Heli')
        self.assertEqual(first_name_response.status_code, 200)

        username_response = self.update_profile('username', 'heli_shah')
        self.assertEqual(username_response.status_code, 200)

    def test_delete_profile_unsuccessful(self):
        """
        delete profile fails if user is not authenticated
        """
        response = self.client.delete(self.profile_url)
        self.assertEqual(response.status_code, 401)

    def test_delete_profile_successful(self):
        """
        delete profile successful
        """
        user = User.objects.get(username='test')
        self.client.force_authenticate(user=user)

        response = self.client.delete(self.profile_url)
        self.assertEqual(response.status_code, 204)


