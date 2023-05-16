from rest_framework import response, status
from test.base import TestViewSetBase


class TestUserViewSet(TestViewSetBase):
    basename = "users"
    create_attributes = {
        "username": "monamari",
        "first_name": "Marina",
        "last_name": "Babe",
        "email": "marina@babe.com",
        "date_of_birth": "2000-01-01",
        "phone": "+79000000001",
    }

    @staticmethod
    def expected_details(entity: dict, attributes: dict):
        return {**attributes, "id": entity["id"]}

    def test_create(self):
        user = self.create(self.create_attributes)
        expected_response = self.expected_details(user, self.create_attributes)
        assert user == expected_response

    def test_list(self):
        admin = self.create_superuser(self.admin_attributes)
        user = self.list(self.user_attributes.get("args"))
        expected_response = [
            self.expected_details({"id": self.user.id}, self.user_attributes),
            self.expected_details({"id": admin.id}, self.admin_attributes),
        ]
        assert user == expected_response

    def test_retrieve(self):
        user = self.retrieve(self.user.id)
        retrieved_user = self.expected_details(
            {"id": self.user.id}, self.user_attributes
        )
        assert user == retrieved_user

    def test_update(self):
        data = self.user_attributes.copy()
        data["first_name"] = "Galina"
        user = self.update(key=self.user.id, data=data)
        retrieved_user = self.expected_details({"id": self.user.id}, data)
        assert user == retrieved_user

    def test_delete(self):
        self.delete(self.user.id)
        list = self.list()
        expected_response = [
            self.expected_details({"id": self.admin.id}, self.admin_attributes),
        ]
        assert list == expected_response

    def test_user_delete(self):
        self.user_delete(self.user.id)

    def test_filter(self):
        self.create_superuser(self.admin_attributes)
        filter_list = self.filter("username", self.user.username)
        expected_response = [
            self.expected_details({"id": self.user.id}, self.user_attributes),
        ]
        assert filter_list == expected_response
