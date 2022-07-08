import pytest
from django.urls import reverse
from rest_framework.test import APIClient


client = APIClient()


class TestUserRegistration:

    @pytest.mark.django_db
    def test_register_user_successful(self):
        payload = {
            "first_name": "heli",
            "last_name": "shah",
            "username": "heli",
            "email": "heli@gmail.com",
            "contact_number": "+919876543210",
            "password": "Abc@1234",
            "password2": "Abc@1234"
        }

        response = client.post(reverse('register'), payload)
        assert response.data['msg'] == 'Registration successful'
        assert response.status_code == 201

    @pytest.mark.django_db
    def test_register_user_fails_if_no_data(self):
        response = client.post(reverse('register'))
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_register_user_with_same_email(self, create_user):
        payload = {
            "first_name": "abc",
            "last_name": "shah",
            "username": "heli",
            "email": "heli@gmail.com",
            "phone_number": "+918670777787",
            "password": "Abcd@1234",
            "password2": "Abcd@1234"
        }
        response = client.post(reverse('register'), payload)
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_register_user_fails(self):
        """
        password doesn't match
        """
        payload = {
            "first_name": "heli",
            "last_name": "shah",
            "username": "heli",
            "email": "heli@gmail.com",
            "contact_number": "+919876543210",
            "password": "Abc@12345",
            "password2": "Abc@1234"
        }

        response = client.post(reverse('register'), payload)
        assert response.status_code == 400


class TestUserLogin:
    @pytest.mark.django_db
    def test_login_user(self, create_user):
        login_data = {
            "email": "heli@gmail.com",
            "password": "Abc@1234"
        }
        response = client.login(email='heli@gmail.com', password='Abc@1234')
        print(response)