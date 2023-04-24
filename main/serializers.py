from rest_framework import serializers

from main.models import User, Tag, Task


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'date_of_birth', 'phone',)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')


class TaskSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    doer = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = (
            'id', 'name', 'description', 'author',
            'doer', 'date_create', 'date_change',
            'status', 'priority', 'tags'
        )
