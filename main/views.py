from rest_framework import viewsets

from main.filters import UserFilter, TaskFilter
from main.models import User, Tag, Task
from main.serializers import UserSerializer, TagSerializer, TaskSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.order_by("id")
    serializer_class = UserSerializer
    filterset_class = UserFilter


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.select_related('author', 'doer').prefetch_related('tags').all()
    serializer_class = TaskSerializer
    filterset_class = TaskFilter

