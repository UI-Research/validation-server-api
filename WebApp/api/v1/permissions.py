from rest_framework import permissions

class IsOwnerOrNoAccess(permissions.BasePermission):
    """ 
    Object-level permission to only allow owners of an object to view it.
    """
    def has_object_permission(self, request, view, obj):
        return obj.researcher_id == request.user
