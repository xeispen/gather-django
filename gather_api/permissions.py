from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit itself.
    """

    def has_object_permission(self, request, view, obj):
        # Read only permissions are allowed to any request
        # allow GET, HEAD, OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet
        return  obj.owner == request.user
