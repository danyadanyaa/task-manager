from http import HTTPStatus
from typing import Union, List

from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient
from main.models import User, Tag, Task

from test.factories import UserFactory, AdminFactory


class TestViewSetBase(APITestCase):
    user: User = None
    admin: User = None
    client: APIClient = None
    basename: str

    user_attributes = UserFactory.build()

    admin_attributes = AdminFactory.build()

    tag_attributes = {
        "name": "tag_test",
    }

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.user = cls.create_api_user(cls.user_attributes)
        cls.tag = cls.create_tag(cls.tag_attributes)
        cls.client = APIClient()

    @staticmethod
    def create_api_user(user_attributes):
        return User.objects.create(**user_attributes)

    @staticmethod
    def create_tag(tag_attributes):
        return Tag.objects.create(**tag_attributes)

    @staticmethod
    def create_superuser(admin_attributes):
        return User.objects.create_superuser(**admin_attributes)

    @classmethod
    def detail_url(cls, key: Union[int, str]) -> str:
        return reverse(f"{cls.basename}-detail", args=[key])

    @classmethod
    def list_url(cls, args: List[Union[str, int]] = None) -> str:
        return reverse(f"{cls.basename}-list", args=args)

    @classmethod
    def list_url_filter(
        cls, filter_name, value, args: List[Union[str, int]] = None
    ) -> str:
        url = reverse(f"{cls.basename}-list")
        return f"{url}?{filter_name}={value}"

    def create(self, data: dict, args: List[Union[str, int]] = None) -> dict:
        self.client.force_authenticate(self.user)
        response = self.client.post(self.list_url(args), data=data)
        return response.json()

    def list(self, args: List[Union[str, int]] = None) -> dict:
        self.client.force_authenticate(self.user)
        response = self.client.get(self.list_url(args=args))
        assert response.status_code == HTTPStatus.OK
        return response.json()

    def retrieve(self, key: Union[int, str] = None) -> dict:
        self.client.force_authenticate(self.user)
        response = self.client.get(self.detail_url(key))
        assert response.status_code == HTTPStatus.OK, response.content
        return response.json()

    def update(self, data: dict, key: Union[int, str] = None) -> dict:
        self.client.force_authenticate(self.user)
        response = self.client.put(self.detail_url(key=key), data=data)
        assert response.status_code == HTTPStatus.OK, response.content
        return response.json()

    def delete(self, key: Union[int, str]) -> dict:
        self.admin = self.create_superuser(self.admin_attributes)
        self.client.force_authenticate(self.admin)
        response = self.client.delete(self.detail_url(key))
        assert response.status_code == HTTPStatus.NO_CONTENT, response.content
        return response

    def user_delete(self, key: Union[int, str]) -> dict:
        self.client.force_authenticate(self.user)
        response = self.client.delete(self.detail_url(key))
        assert response.status_code == HTTPStatus.FORBIDDEN, response.content
        return response

    def unauthorized_access(
        self, data: dict, args: List[Union[str, int]] = None
    ) -> dict:
        self.client.logout()
        response = self.client.post(self.list_url(args), data=data)
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        return response

    def filter(self, filter_name, value, args: List[Union[str, int]] = None):
        self.client.force_authenticate(self.user)
        response = self.client.get(
            self.list_url_filter(filter_name=filter_name, value=value, args=args)
        )
        assert response.status_code == HTTPStatus.OK
        return response.json()
