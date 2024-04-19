# In case of using the 'manager_group' permission: 
# copy-paste this code into the 'permissions.py' file 
# and adapt the import and the call in the views.py file 


# # Put this into mixins in order to use 'manager_group' group 
# def get_users_groups(request): 
#     """ Get the list of the request.user's groups 
#         Args:
#             request (request) 
#         Returns:
#             groups_as_list: list of strings 
#     """ 
#     users_groups = request.user.groups.values_list('name', flat = True) 
#     groups_as_list = list(users_groups) 
#     # print(str(request.user) + ' permissions : ' + str(groups_as_list)) 
#     return groups_as_list 


# class IsManagerGroup(permissions.BasePermission): 
#     """ permission class that permits only managers to request on urls 
#         Args:
#             permissions (permissions): class that defines the permissions and their conditions 
#     """ 

#     def has_permission(self, request, view): 

#         groups_as_list = get_users_groups(request) 
#         if len(groups_as_list) > 0:  
#             if 'manager_group' in groups_as_list: 
#                 return True 
#         else: 
#             return False 



