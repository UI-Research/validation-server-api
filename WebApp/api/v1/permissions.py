from rest_framework import permissions

class IsOwnerOrNoAccess(permissions.BasePermission):
    """ 
    Object-level permission to only allow owners of an object to view it.
    """
    def has_object_permission(self, request, view, obj):
        return obj.researcher == request.user

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    The request is authenticated as admin, or is a read-only request.
    """
    def has_permission(self, request, view):
        if (request.method in ['GET'] or
            (request.user and
            request.user.groups.filter(name='Administrator'))):
            return True
        return False

#class IsDataSteward(permissions.BasePermission):
#    def has_permission(self, request, view):
#        if request.user and request.user.groups.filter(name='DataSteward'):
#            return True
#        return False
#
class IsAdministrator(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.groups.filter(name='Administrator'):
            return True
        return False


    
#class IsResearcher(permissions.BasePermission):
#    def has_permission(self, request, view):
#        if request.user and request.user.groups.filter(name='Researcher'):
#            return True
#        return False
#
#def is_in_group(user, group_name):
#    """    
#    Takes a user and a group name, and returns `True` if the user is in that group.
#    """
#    try:
#        return Group.objects.get(name=group_name).user_set.filter(id=user.id).exists()
#    except Group.DoesNotExist:
#        return None
#

