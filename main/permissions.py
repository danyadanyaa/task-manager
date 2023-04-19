from rest_framework import permissions


class IsStaffDeleteOrAuth(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == "DELETE":
            return request.user.is_staff
        if request.method == "POST":
            return request.user.is_authenticated
        return request.user.is_authenticated
