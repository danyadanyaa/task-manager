from django.core.files.uploadedfile import SimpleUploadedFile
from test.base import TestViewSetBase

from factories import UserFactory, ImageFileProvider


class TestUserViewSet(TestViewSetBase):
    basename = "users"

    @staticmethod
    def expected_details(entity: dict, attributes: dict):
        return {**attributes, "id": entity["id"], 'avatar_picture': entity['avatar_picture']}

    def test_create(self):
        user_attributes = UserFactory.build()
        user = self.create(user_attributes)
        del user_attributes['password']
        expected_response = self.expected_details(user, user_attributes)
        assert user == expected_response

    def test_list(self):
        pre_user = self.retrieve(self.user.id)
        another_user_attributes = UserFactory.build()
        another_user = self.create(another_user_attributes)
        del another_user_attributes['password']
        user_list = self.list(self.user_attributes.get("args"))
        expected_response = [
            self.expected_details(pre_user, self.user_attributes),
            self.expected_details(another_user, another_user_attributes),
        ]
        assert user_list == expected_response

    def test_retrieve(self):
        user = self.retrieve(self.user.id)
        retrieved_user = self.expected_details(
            user, self.user_attributes
        )
        assert user == retrieved_user

    def test_update(self):
        data = UserFactory.build()
        an_data = UserFactory.build()
        user_data = self.create(data)
        data['first_name'] = 'Galina'
        data['avatar_picture'] = an_data['avatar_picture']
        self.update(key=user_data['id'], data=data)
        del data['password']
        user = self.retrieve(user_data['id'])
        retrieved_user = self.expected_details(user, data)
        assert user == retrieved_user

    def test_delete(self):
        self.delete(self.user.id)
        admin = self.retrieve(self.admin.id)
        admin_attributes = self.admin_attributes
        for key in ['password', 'is_staff', 'is_superuser']:
            del admin_attributes[key]
        user_list = self.list()
        expected_response = [
            self.expected_details(admin, admin_attributes),
        ]
        assert user_list == expected_response

    def test_user_delete(self):
        self.user_delete(self.user.id)

    def test_filter(self):
        self.create_superuser(self.admin_attributes)
        filter_list = self.filter("username", self.user.username)
        user = self.retrieve(self.user.id)
        expected_response = [
            self.expected_details(user, self.user_attributes),
        ]
        assert filter_list == expected_response

    def test_large_avatar(self) -> None:
        user_attributes = UserFactory.build(
            avatar_picture=SimpleUploadedFile("large.jpg", b"x" * 2 * 1024 * 1024)
        )
        response = self.create(user_attributes)
        assert response == {"avatar_picture": ["Maximum size 1048576 exceeded."]}

    def test_avatar_bad_extension(self) -> None:
        user_attributes = UserFactory.build()
        user_attributes["avatar_picture"].name = "bad_extension.pdf"
        response = self.create(user_attributes)
        assert response == {
            "avatar_picture": [
                "File extension “pdf” is not allowed. Allowed extensions are: jpeg, jpg, png."
            ]
        }


