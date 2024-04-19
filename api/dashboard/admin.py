from dashboard.models import (
    Client_profile, Bei_profile, Address, Site, Client, Bei, 
    Maintenance, Installation, 
) 
from data_acquisition.models import Door_event, Data_acquisition  
from django.contrib import admin 
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User


# Override UserAdmin in order to 
# custom displaying its columns in admin itf 
class UserAdmin(BaseUserAdmin): 
    list_display = ('id', 'username', 'groups_ids', 'groups_names', 'is_staff') 

    # en-tête de colonnes : 
    def groups_ids(self, user): 

        user_group_ids = user.groups.values_list('id', flat = True)      # QuerySet Object  
        group_ids_as_list = list(user_group_ids)                        # QuerySet to `list`

        text = group_ids_as_list  
        return text 
    groups_ids.short_description = 'Groups ids'

    def groups_names(self, user): 

        user_group_names = user.groups.values_list('name', flat = True)  # QuerySet Object 
        group_names_as_list = list(user_group_names)                    # QuerySet to `list` 

        text = group_names_as_list  
        return text 
    groups_names.short_description = 'Groups names' 

# Re-register UserAdmin
admin.site.unregister(User) 
admin.site.register(User, UserAdmin) 

class Client_profileAdmin(admin.ModelAdmin): 
    list_display = ('id', 'client_user', 'client') 
admin.site.register(Client_profile, Client_profileAdmin) 

class Bei_profileAdmin(admin.ModelAdmin): 
    list_display = ('id', 'bei_user', 'bei') 
admin.site.register(Bei_profile, Bei_profileAdmin) 

class AdressAdmin(admin.ModelAdmin): 
    list_display = ('id', 'city', 'updated_at') 
admin.site.register(Address, AdressAdmin) 

class SiteAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address')
admin.site.register(Site, SiteAdmin) 

class ClientAdmin(admin.ModelAdmin): 
    list_display = ('id', 'name', 'password', 'updated_at') 
admin.site.register(Client, ClientAdmin) 

class BeiAdmin(admin.ModelAdmin): 
    list_display = ('id', 'serial_number', 'client', 'password') 
admin.site.register(Bei, BeiAdmin)  

class MaintenanceAdmin(admin.ModelAdmin): 
    list_display = ('id', 'maintenance_name', 'bei')
admin.site.register(Maintenance, MaintenanceAdmin) 

class InstallationAdmin(admin.ModelAdmin): 
    list_display = ('id', 'site', 'bei') 
admin.site.register(Installation, InstallationAdmin) 

# data_acquisition app 
class Door_eventAdmin(admin.ModelAdmin): 
    list_display = ('time', 'bei') 
admin.site.register(Door_event, Door_eventAdmin) 

class Data_acquisitionAdmin(admin.ModelAdmin): 
    list_display = ('time', 'bei') 
admin.site.register(Data_acquisition, Data_acquisitionAdmin) 


