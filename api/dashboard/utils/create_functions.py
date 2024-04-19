from dashboard.models import ( 
    Address, Bei, Client, Installation, Maintenance, Site 
) 
# functions 
from django.contrib.auth.hashers import make_password 
# utils 
from datetime import datetime 


def create_address(data): 
    new_address = Address(
        city=data['city'], 
        zipcode=data['zipcode'], 
        street=data['street'], 
        street_number=data['street_number'], 
        lat=data['lat'], 
        lng=data['lng'] 
    ) 
    new_address.save() 
    print(f'new_address DV280 : {Address.objects.last()}') 
    return new_address 


def create_site(data): 
    new_site = Site( 
        name=data['city'], 
        address = Address.objects.last()  
    ) 
    new_site.save() 
    print(f'new_site DV283 : {Site.objects.last()}') 
    return new_site 


def create_bei(data): 
    new_bei = Bei( 
        serial_number = data['serial_number'], 
        fuel_capacity= data["fuel_capacity"], 
        client=Client.objects.get(id=data['client']), 
        password=make_password(data["password"]) 
    ) 
    new_bei.save() 
    print(f'new_bei DV286 : {Bei.objects.last()}') 
    return new_bei 


def create_installation(data): 
    new_installation = Installation( 
        site=Site.objects.last(), 
        bei=Bei.objects.last(), 
        installation_date=data['installation_date'] 
    ) 
    new_installation.save() 
    print(f'site last : {Site.objects.last()}') 
    print(f'bei : {Bei.objects.last()}') 
    print(f'new installation : {new_installation} created') 
    return new_installation 


def create_maintenance(data): 
    new_maintenance = Maintenance( 
        bei=Bei.objects.last(), 
        description=f'Installation sur site {data["serial_number"]}', 
        maintenance_name='Installation', 
        maintenance_date=data["maintenance_date"] 
    ) 
    new_maintenance.save() 
    print(f'new_maintenance DV292 : {Maintenance.objects.last()}') 
    return new_maintenance 

