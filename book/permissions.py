from rest_framework import permissions


class IsOwnerOrStaffOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # GET, HEAD or OPTIONS requests are allowed to all
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of record
        # or 'is_staff' user.
        return obj.owner == request.user or request.user.is_staff


class IsStaffOrReadPutOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        # PUT is allowed on the viewset level
        if request.method in ('GET', 'HEAD', 'PUT', 'OPTIONS'):
            return True
        return request.user.is_staff

    def has_object_permission(self, request, view, obj):
        # But write permissions only allowed to the owner (to PUT) of record
        # or 'is_staff' user (all permissions)
        return request.user.is_staff or request.user.username == obj.username
