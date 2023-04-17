from django.db import models
from .user import User
from .tag import Tag


class Task(models.Model):
    class Statuses(models.TextChoices):
        NEW_TASK = "new_task"
        IN_DEVELOPMENT = "in_development"
        IN_QA = "in_qa"
        IN_CODE_REVIEW = "in_code_review"
        READY_FOR_RELEASE = "ready_for_release"
        RElEASED = "released"
        ARCHIVED = "archived"

    class Priorities(models.TextChoices):
        HIGH = "High"
        MEDIUM = "Medium"
        LOW = "Low"
        NO_PRIORITY = "None"

    name = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(max_length=1000, verbose_name="Описание")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    doer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="task_doer")
    date_create = models.DateField(auto_now_add=True, verbose_name="Дата создания")
    date_change = models.DateField(auto_now=True, verbose_name="Дата изменения")
    date_deadline = models.DateField(blank=True, null=True, verbose_name="Deadline")
    status = models.CharField(
        max_length=255, default=Statuses.NEW_TASK, choices=Statuses.choices
    )
    priority = models.CharField(
        max_length=255, default=Priorities.NO_PRIORITY, choices=Priorities.choices
    )
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name
