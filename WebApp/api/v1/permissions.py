from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """ 
    Object-level permission to only allow owners of an object to view it.
    """
    def has_object_permission(self, request, view, obj):
        return obj.researcher_id == request.user


class IsAdministrator(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.groups.filter(name='Administrators'):
            return True
        return False
