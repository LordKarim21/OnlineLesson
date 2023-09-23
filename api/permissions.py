from rest_framework import permissions


class IsProductOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class HasAccessToProductORIsProductOwner(IsProductOwner):
    def has_object_permission(self, request, view, obj):
        return request.user in obj.users.all() or super().has_object_permission(request, view, obj)
