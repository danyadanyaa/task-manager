from datetime import timedelta

from freezegun.api import freeze_time
from rest_framework import status
from django.urls import reverse
from rest_framework.test import APITestCase

from factories import UserFactory

from main.models import User


class TestJWTAuth(APITestCase):
    token_url = reverse("token_obtain_pair")
    refresh_token_url = reverse("token_refresh")
    any_api_url = "/api/tasks/"

    @staticmethod
    def create_user():
        user_attr = UserFactory.build()
        User.objects.create_user(**user_attr)
        return user_attr

    def token_request(self, username: str = None, password: str = None):
        client = self.client_class()
        if not username:
            user = self.create_user()
            username = user['username']
            password = user['password']
        return client.post(self.token_url, data={"username": username, "password": password})

    def refresh_token_request(self, refresh_token: str):
        client = self.client_class()
        return client.post(self.refresh_token_url, data={"refresh": refresh_token})

    def get_refresh_token(self):
        response = self.token_request()
        return response.json()["refresh"]

    def test_successful_auth(self):
        response = self.token_request()
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["refresh"]
        assert response.json()["access"]

    def test_unsuccessful_auth(self):
        response = self.token_request(username="incorrect_username", password="incorrect_password")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_refresh_token(self):
        refresh_token = self.get_refresh_token()
        response = self.refresh_token_request(refresh_token)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["access"]

    def test_token_auth(self) -> None:
        client = self.client_class()
        response = client.get(self.any_api_url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        response = self.token_request()
        token = response.json()["access"]
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = client.get(self.any_api_url)
        assert response.status_code == status.HTTP_200_OK

    def test_refresh_lives_lower_than_one_day(self) -> None:
        with freeze_time() as frozen_time:
            refresh_token = self.get_refresh_token()
            frozen_time.tick(timedelta(hours=23, minutes=59))
            response = self.refresh_token_request(refresh_token)
            assert response.status_code == status.HTTP_200_OK
            assert response.json()["access"]

    def test_refresh_dies_after_one_day(self) -> None:
        with freeze_time() as frozen_time:
            refresh_token = self.get_refresh_token()
            frozen_time.tick(timedelta(days=1))
            response = self.refresh_token_request(refresh_token)
            assert response.status_code == status.HTTP_401_UNAUTHORIZED

