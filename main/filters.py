from django_filters import rest_framework as filters

from main.models import User, Tag, Task


class UserFilter(filters.FilterSet):
    username = filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = User
        fields = ("username",)


class TaskFilter(filters.FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(), field_name="tags__name", to_field_name="name"
    )
    status = filters.CharFilter(lookup_expr="iexact")
    author = filters.CharFilter(field_name="author__username", lookup_expr="icontains")
    doer = filters.CharFilter(field_name="doer__username", lookup_expr="icontains")

    class Meta:
        model = Task
        fields = (
            "status",
            "tags",
            "doer",
            "author",
        )
