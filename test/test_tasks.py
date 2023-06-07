import datetime

from rest_framework import response, status
from test.base import TestViewSetBase

from main.models import Task, User


class TestUserViewSet(TestViewSetBase):
    basename = "tasks"
    task_attributes = {
        "name": "new_task",
        "description": "Some new task",
        "date_create": datetime.date.today().strftime("%Y-%m-%d"),
        "date_change": datetime.date.today().strftime("%Y-%m-%d"),
        "date_deadline": "2023-06-06",
        "status": "new_task",
        "priority": "High",
    }

    @staticmethod
    def expected_usr_tag(entity: dict, attributes: dict):
        return {**attributes, "id": entity["id"]}

    @staticmethod
    def expected_details(entity: dict, attributes: dict):
        return {
            **attributes,
            "id": entity["id"],
            "author": entity["author"],
            "doer": entity["doer"],
            "tags": entity["tags"],
        }

    @staticmethod
    def make_data(entity: dict, attributes: dict):
        return {**attributes, "doer": entity["doer"], "tags": entity["tags"]}

    def test_create(self):
        task = self.create(
            self.make_data(
                {"doer": self.user.id, "tags": [self.tag.id]}, self.task_attributes
            )
        )
        expected_response = self.expected_details(
            {
                "id": task["id"],
                "doer": self.expected_usr_tag(
                    {"id": self.user.id}, self.user_attributes
                ),
                "author": self.expected_usr_tag(
                    {"id": self.user.id}, self.user_attributes
                ),
                "tags": [
                    self.expected_usr_tag({"id": self.tag.id}, self.tag_attributes)
                ],
            },
            self.task_attributes,
        )
        assert task == expected_response

    def test_list(self):
        task = self.create(
            self.make_data(
                {"doer": self.user.id, "tags": [self.tag.id]}, self.task_attributes
            )
        )
        another_task = self.create(
            self.make_data(
                {"doer": self.user.id, "tags": [self.tag.id]}, self.task_attributes
            )
        )
        tasks = self.list()
        expected_response = [
            self.expected_details(
                {
                    "id": task["id"],
                    "doer": self.expected_usr_tag(
                        {"id": self.user.id}, self.user_attributes
                    ),
                    "author": self.expected_usr_tag(
                        {"id": self.user.id}, self.user_attributes
                    ),
                    "tags": [
                        self.expected_usr_tag({"id": self.tag.id}, self.tag_attributes)
                    ],
                },
                self.task_attributes,
            ),
            self.expected_details(
                {
                    "id": another_task["id"],
                    "doer": self.expected_usr_tag(
                        {"id": self.user.id}, self.user_attributes
                    ),
                    "author": self.expected_usr_tag(
                        {"id": self.user.id}, self.user_attributes
                    ),
                    "tags": [
                        self.expected_usr_tag({"id": self.tag.id}, self.tag_attributes)
                    ],
                },
                self.task_attributes,
            ),
        ]
        assert tasks == expected_response

    def test_retrieve(self):
        task = self.create(
            self.make_data(
                {"doer": self.user.id, "tags": [self.tag.id]}, self.task_attributes
            )
        )
        task_retrieve = self.retrieve(task["id"])
        retrieved_task = self.expected_details(
            {
                "id": task["id"],
                "doer": self.expected_usr_tag(
                    {"id": self.user.id}, self.user_attributes
                ),
                "author": self.expected_usr_tag(
                    {"id": self.user.id}, self.user_attributes
                ),
                "tags": [
                    self.expected_usr_tag({"id": self.tag.id}, self.tag_attributes)
                ],
            },
            self.task_attributes,
        )
        assert task_retrieve == retrieved_task

    def test_update(self):
        data = self.make_data(
            {"doer": self.user.id, "tags": [self.tag.id]}, self.task_attributes
        )
        task = self.create(data)
        data["name"] = "updated_task"
        task_update = self.update(key=task["id"], data=data)
        retrieved_task = self.expected_details(
            {
                "id": task["id"],
                "doer": self.expected_usr_tag(
                    {"id": self.user.id}, self.user_attributes
                ),
                "author": self.expected_usr_tag(
                    {"id": self.user.id}, self.user_attributes
                ),
                "tags": [
                    self.expected_usr_tag({"id": self.tag.id}, self.tag_attributes)
                ],
            },
            data,
        )
        assert task_update == retrieved_task

    def test_delete(self):
        task = self.create(
            self.make_data(
                {"doer": self.user.id, "tags": [self.tag.id]}, self.task_attributes
            )
        )
        another_task = self.create(
            self.make_data(
                {"doer": self.user.id, "tags": [self.tag.id]}, self.task_attributes
            )
        )
        self.delete(another_task["id"])
        list = self.list()
        expected_response = [
            self.expected_details(
                {
                    "id": task["id"],
                    "doer": self.expected_usr_tag(
                        {"id": self.user.id}, self.user_attributes
                    ),
                    "author": self.expected_usr_tag(
                        {"id": self.user.id}, self.user_attributes
                    ),
                    "tags": [
                        self.expected_usr_tag({"id": self.tag.id}, self.tag_attributes)
                    ],
                },
                self.task_attributes,
            )
        ]
        assert list == expected_response

    def test_user_delete(self):
        task = self.create(
            self.make_data(
                {"doer": self.user.id, "tags": [self.tag.id]}, self.task_attributes
            )
        )
        self.user_delete(task["id"])

    def test_unauthorized_access(self):
        data = self.make_data(
            {"doer": self.user.id, "tags": [self.tag.id]}, self.task_attributes
        )
        self.unauthorized_access(data)

    def test_filters(self):
        data = self.make_data(
            {"doer": self.user.id, "tags": [self.tag.id]}, self.task_attributes
        )
        self.create(data)
        data["status"] = "in_development"
        another_task = self.create(data)
        task_filter = self.filter("status", another_task["status"])
        expected_response = [
            self.expected_details(
                {
                    "id": another_task["id"],
                    "doer": self.expected_usr_tag(
                        {"id": self.user.id}, self.user_attributes
                    ),
                    "author": self.expected_usr_tag(
                        {"id": self.user.id}, self.user_attributes
                    ),
                    "tags": [
                        self.expected_usr_tag({"id": self.tag.id}, self.tag_attributes)
                    ],
                },
                data,
            )
        ]
        assert task_filter == expected_response
