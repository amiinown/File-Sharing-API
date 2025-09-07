from rest_framework.permissions import BasePermission, SAFE_METHODS
from group.models import UserGroupPermission, Group

class BaseGroupPermission(BasePermission):
    """
    Base permission class for group-related permissions.
    Provides utility methods to check if a user is the owner or a member of a group.

    methods:
        is_owner(user, obj): Check if the user is the owner of the object.
        is_member(user, obj): Check if the user is a member of the group object.
        has_safe_method(request): Check if the request method is safe (GET, HEAD, OPTIONS).
    """

    def is_owner(self, user, obj):
        return user == obj.owner

    def is_member(self, user, obj):
        if isinstance(obj, Group):
            return obj.members.filter(pk=user.pk).exists()
        return False

    def has_safe_method(self, request):
        return request.method in SAFE_METHODS


class IsGroupOwner(BaseGroupPermission):
    message = 'You need to be group owner.'

    def has_object_permission(self, request, view, obj):
        if self.has_safe_method(request):
            return True
        return self.is_owner(request.user, obj)


class IsGroupOwnerOrMember(BaseGroupPermission):
    message = 'You need to be group owner or member.'

    def has_object_permission(self, request, view, obj):
        if self.has_safe_method(request):
            return True

        if isinstance(obj, Group):
            return self.is_owner(request.user, obj) or self.is_member(request.user, obj)
        return False


class IsGroupOwnerOrReadWriteMember(BaseGroupPermission):
    message = 'You need to be owner or Read & Write member.'

    def has_object_permission(self, request, view, obj):
        if self.has_safe_method(request):
            return True

        if isinstance(obj, Group):
            return (
                self.is_owner(request.user, obj) or
                obj.user_permissions.filter(
                    user=request.user,
                    permission=UserGroupPermission.Role.READ_WRITE
                ).exists()
            )
        return False