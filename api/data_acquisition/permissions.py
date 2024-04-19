from rest_framework import permissions 


def get_users_groups(request): 
    """ Get the list of the request.user's groups 
        Args:
            request (request) 
        Returns:
            groups_as_list: list of strings 
    """ 
    users_groups = request.user.groups.values_list('name', flat = True) 
    groups_as_list = list(users_groups) 
    return groups_as_list 


class IsBeiGroup(permissions.BasePermission): 
    """ permission class that permits only Beis to send requests on urls 
        Args:
            permissions (permissions): class that defines the permissions and their conditions 
    """ 

    def has_permission(self, request, view): 

        groups_as_list = get_users_groups(request) 
        if len(groups_as_list) > 0:  
            if 'bei_group' in groups_as_list: 
                return True 
        else: 
            print('group pas ok') 
            return False 


