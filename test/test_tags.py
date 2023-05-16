from rest_framework import response, status
from test.base import TestViewSetBase


class TestUserViewSet(TestViewSetBase):
    basename = "tags"
    another_tag_attributes = {
        "name": "another_tag",
    }

    @staticmethod
    def expected_details(entity: dict, attributes: dict):
        return {**attributes, "id": entity["id"]}

    def test_create(self):
        tag = self.create(self.tag_attributes)
        expected_response = self.expected_details(tag, self.tag_attributes)
        assert tag == expected_response

    def test_list(self):
        another_tag = self.create_tag(self.another_tag_attributes)
        tags = self.list()
        expected_response = [
            self.expected_details({"id": self.tag.id}, self.tag_attributes),
            self.expected_details({"id": another_tag.id}, self.another_tag_attributes),
        ]
        assert tags == expected_response

    def test_retrieve(self):
        tag = self.retrieve(self.tag.id)
        retrieved_tag = self.expected_details({"id": self.tag.id}, self.tag_attributes)
        assert tag == retrieved_tag

    def test_update(self):
        data = self.tag_attributes.copy()
        data["name"] = "updated_tag"
        tag = self.update(key=self.tag.id, data=data)
        retrieved_tag = self.expected_details({"id": self.tag.id}, data)
        assert tag == retrieved_tag

    def test_delete(self):
        another_tag = self.create_tag(self.another_tag_attributes)
        self.delete(self.tag.id)
        list = self.list()
        expected_response = [
            self.expected_details({"id": another_tag.id}, self.another_tag_attributes),
        ]
        assert list == expected_response

    def test_user_delete(self):
        self.user_delete(self.tag.id)

    def test_unauthorized_access(self):
        self.unauthorized_access(self.tag_attributes)
