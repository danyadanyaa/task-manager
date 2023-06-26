import datetime

from unittest.mock import patch, MagicMock


from django.core import mail
from django.template.loader import render_to_string


from main.models import Task, Tag
from main.services.mail import send_assign_notification
from test.base import TestViewSetBase


class TestSendEmail(TestViewSetBase):
    tag: Tag = None
    task: Task = None
    basename: str = 'tasks'

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
    def make_data(entity: dict, attributes: dict):
        return {**attributes, "doer": entity["doer"], "tags": entity["tags"]}

    def setUp(self) -> None:
        super().setUp()
        self.task = self.create(
            self.make_data(
                {"doer": self.user.id, "tags": [self.tag.id]}, self.task_attributes
            )
        )

    @patch.object(mail, "send_mail")
    def test_send_assign_notification(self, fake_sender: MagicMock) -> None:
        assignee = self.user
        task = self.task

        send_assign_notification(task["id"])

        fake_sender.assert_called_once_with(
            subject="You've assigned a task.",
            message="",
            from_email=None,
            recipient_list=[assignee.email],
            html_message=render_to_string(
                "emails/notification.html",
                context={"task": Task.objects.get(pk=task["id"])},
            ),
        )
