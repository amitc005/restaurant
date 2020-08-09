import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User


@pytest.mark.django_db
class TestTodoAPI:
    @pytest.fixture(autouse=True)
    def setUp(self):
        login_data = {"username": "testuser", "password": "abc123"}
        user = User.objects.create_user(**login_data)
        self.client = APIClient()
        self.client.force_authenticate(user=user)
