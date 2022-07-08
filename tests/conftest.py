import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from accounts.models import User


@pytest.fixture
def create_user():
    user, created = User.objects.get_or_create(first_name="heli", last_name="shah", username="heli",
                                               email="heli@gmail.com",
                                               contact_number="+919876543210")
    if created:
        print(f'Total users in database: {User.objects.all().count()}')
        print(f'Primary key: {user.pk}')
        user.set_password(raw_password='Abc@1234')
        user.save()
    return user
