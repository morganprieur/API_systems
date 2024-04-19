from django.db import models
from django.contrib.auth.models import User 

import datetime 


class Address(models.Model):
    city = models.CharField(max_length = 45)
    zipcode = models.CharField(max_length = 10)
    street = models.CharField(max_length = 45)
    street_number = models.CharField(
        max_length = 20, 
        blank = True,
        null = True
    ) 
    suplement = models.CharField(
        max_length = 45, 
        blank = True,
        null = True
    )
    lat = models.FloatField()
    lng = models.FloatField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True) 

    def __str__(self): 
        return f'{self.city}' 

class Site(models.Model): 
    """ Table to store the BETIs' localisation sites """
    name = models.CharField(max_length = 45, blank = True, null = True, default='999') 
    address = models.OneToOneField( 
        Address, 
        on_delete = models.SET_NULL,
        blank = True,
        null = True, 
        related_name = 'site_address' 
    ) 
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True) 

    def __str__(self): 
        return f'{self.name}' 

class Client(models.Model): 
    name = models.CharField(max_length = 45) 
    password = models.CharField(max_length=100) 
    created_at = models.DateTimeField(auto_now_add = True) 
    updated_at = models.DateTimeField(auto_now = True) 

    def __str__(self): 
        return f'{self.id}'

class Bei(models.Model): 
    serial_number = models.CharField(max_length = 45)
    fuel_capacity = models.IntegerField() 
    client = models.ForeignKey(
        Client,
        on_delete = models.SET_NULL,
        blank = True,
        null = True, 
        related_name='bei' 
    ) 
    password = models.CharField(max_length=100) 
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models. DateTimeField(auto_now = True) 

    def __str__(self): 
        return f'{self.serial_number}' 

class Bei_profile(models.Model): 

    bei_user = models.OneToOneField(
        'auth.User', 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name = 'bei_profile_user' 
    ) 
    bei = models.ForeignKey(
        'dashboard.Bei', 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name = 'bei_profile' 
    ) 

    def __str__(self): 
        return f'{self.bei.serial_number}' 

class Client_profile(models.Model): 

    client_user = models.OneToOneField(
        'auth.User', 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='client_profile_user'
    )  
    client = models.ForeignKey(
        'dashboard.Client', 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='client_profile' 
    ) 

    def __str__(self): 
        return f'{self.client_user.username}'

class Installation(models.Model): 
    site = models.ForeignKey(
        Site,
        on_delete = models.SET_NULL,
        blank = True,
        null = True, 
        related_name = 'installation_site' 
    ) 
    bei = models.ForeignKey(
        Bei,
        on_delete = models.CASCADE, 
        related_name = 'installation_bei' 
    ) 
    # 'date' is a django's reserved word  
    installation_date = models.DateTimeField() 
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self): 
        return f'{self.bei}'

class Maintenance(models.Model): 
    bei = models.ForeignKey(
        Bei, 
        on_delete = models.CASCADE, 
        related_name = 'maintenance_bei' 
    ) 
    description = models.CharField(max_length = 45)
    maintenance_name =  models.CharField(max_length=45) 
    # Date de la dernière maintenance : 
    maintenance_date = models.DateTimeField(blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self): 
        return f'{self.maintenance_date}'


