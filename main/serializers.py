from django.shortcuts import get_object_or_404
from rest_framework import serializers

from main.models import User, Tag, Task


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "date_of_birth",
            "phone",
        )


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name")


class TaskViewSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer(many=False, read_only=True)
    doer = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Task
        fields = "__all__"


class TaskSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())
    doer = serializers.PrimaryKeyRelatedField(many=False, queryset=User.objects.all())

    class Meta:
        model = Task
        fields = (
            "id",
            "name",
            "description",
            "doer",
            "date_create",
            "date_change",
            "date_deadline",
            "status",
            "priority",
            "tags",
        )

    def create(self, validated_data):
        user_id = validated_data.pop("doer")
        user_instance = get_object_or_404(User, username=user_id)
        validated_data["doer"] = user_instance
        tags_list = []
        for tag in validated_data.pop("tags"):
            add_tag = get_object_or_404(Tag, name=tag)
            tags_list.append(add_tag)

        new_task = Task.objects.create(**validated_data)
        new_task.tags.set(tags_list)
        return new_task

    def to_representation(self, instance):
        return TaskViewSerializer(
            instance, context={"request": self.context.get("request")}
        ).data
