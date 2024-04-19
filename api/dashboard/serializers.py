from dashboard.models import ( 
    Address, Bei, Bei_profile, Client, Client_profile, 
    Installation, Maintenance, Site 
) 
from django.contrib.auth.models import User 
# utils 
from rest_framework import serializers 
import re 
from datetime import datetime, timedelta 
from django.contrib.auth.hashers import make_password 



class UserSerializer(serializers.ModelSerializer): 

    class Meta: 
        model = User 
        fields = ( 
            'id', 
            'username', 
            'groups' 
        ) 

class ClientSerializer(serializers.ModelSerializer): 
    
    name = serializers.CharField(max_length=45)  
    password = serializers.CharField(max_length=150) 

    class Meta: 
        model = Client 
        fields = ( 
            'id', 
            'name', 
            'password' 
        ) 

    def create(self, validated_data): 
        validated_data['password'] = make_password(validated_data['password']) 
        return Client.objects.create(**validated_data) 

class Client_profileSerializer(serializers.ModelSerializer): 

    client_user = UserSerializer() 
    client = ClientSerializer() 


    class Meta: 
        model = Client_profile 
        fields = ( 
            'client_user', 
            'client', 
        ) 

class AddressSerializer(serializers.ModelSerializer): 

    city = serializers.CharField(max_length=45) 
    zipcode = serializers.CharField(max_length=10) 
    street = serializers.CharField(max_length=45) 
    street_number = serializers.IntegerField() 
    suplement = serializers.CharField( 
        required=False, 
        max_length=45 
    ) 
    lat = serializers.FloatField() 
    lng = serializers.FloatField() 

    class Meta: 
        model = Address 
        fields = (
            'city', 'zipcode', 'street', 'street_number', 
            'suplement', 'lat', 'lng' 
        ) 

class SiteSerializer(serializers.ModelSerializer): 

    name = serializers.CharField(max_length=45) 
    address = AddressSerializer() 

    class Meta: 
        model = Site 
        fields = (
            'name', 
            'address' 
        ) 

class BeiSerializer(serializers.ModelSerializer): 

    serial_number = serializers.CharField(max_length=45) 
    fuel_capacity = serializers.CharField(max_length=45) 
    client = ClientSerializer() 
    password = serializers.CharField(max_length=150) 

    class Meta: 
        model = Bei 
        fields = ( 
            'serial_number', 
            'fuel_capacity', 
            'client', 
            'password' 
        ) 
    
    

class Bei_profileSerializer(serializers.ModelSerializer): 

    bei_user = UserSerializer()  
    bei = BeiSerializer() 

    class Meta: 
        model = Bei_profile 
        fields = ( 
            'bei_user', 
            'bei' 
        ) 

class NewBeiSerializer(serializers.ModelSerializer): 

    serial_number = serializers.CharField(max_length=45) 
    fuel_capacity = serializers.CharField(max_length=45) 
    client = ClientSerializer() 
    password = serializers.CharField(max_length=150) 

    class Meta: 
        model = Bei 
        fields = ( 
            'serial_number', 
            'fuel_capacity', 
            'client', 
            'password' 
        ) 

class InstallationSerializer(serializers.ModelSerializer): 
    
    site = SiteSerializer() 
    bei = BeiSerializer() 
    installation_date = serializers.DateTimeField() 

    class Meta: 
        model = Installation 
        fields = ( 
            'site', 
            'bei', 
            'installation_date' 
        ) 
    
    # Custom create()
    def create(self, validated_data): 
        address_data = validated_data['site'].pop('address') 
        new_address = Address.objects.create(**address_data) 

        site_data = validated_data.pop('site') 
        new_site = Site.objects.create( 
            address=Address.objects.last(), 
            **site_data 
        )

        client_data = validated_data['bei'].pop('client') 

        bei_data = validated_data.pop('bei') 
        new_bei = Bei.objects.create( 
            client=Client.objects.get( 
                name=client_data['name'] 
            ), 
            **bei_data 
        ) 

        new_installation = Installation.objects.create( 
            bei=Bei.objects.last(), 
            site=Site.objects.last(), 
            **validated_data 
        ) 

        return new_installation 
    

class MaintenanceSerializer(serializers.ModelSerializer): 

    site = SiteSerializer() 
    bei = BeiSerializer() 
    installation_date = serializers.DateTimeField() 
    description = serializers.CharField(max_length=45) 
    maintenance_name = serializers.CharField(max_length=45) 
    maintenance_date = serializers.DateTimeField() 

    class Meta: 
        model = Maintenance 
        depth = 1 
        fields = ( 
            'site', 
            'bei', 
            'installation_date', 
            'description', 
            'maintenance_name',  
            'maintenance_date' 
        ) 


class FileUploadSerializer(serializers.Serializer): 
    """ File upload storage 

    Args:
        serializers (_type_): Django Serializer class  
    """
    file = serializers.FileField()


class MetricSerializer(serializers.Serializer): 

    class meta: 
        fields = ( 
            'bei', 
            'maintenance_date' 
        )  
    
    def to_representation(self, instance): 
        maintenance = Maintenance.objects.filter(bei=instance.bei).last() 
        install = Installation.objects.get(bei=instance.bei) 
        siteId = install.site.id 
        siteName = install.site.name 
        dtime = instance.time 
        dt_data_acquisition = re.sub(str(dtime), f'{dtime}.000000', str(dtime)) 
        deltaMaintenance_date = timedelta(days=366/2) 
        var_18 = (maintenance.maintenance_date + deltaMaintenance_date).replace(tzinfo=None) 
        
        metric = super().to_representation(instance) 
        metric['timestamp'] = str(dt_data_acquisition) 
        metric['id'] = { 
            'value': str(siteId), 
            'Type': "Int64", 
            'Valid': True 
        } 
        metric['name'] = { 
            'value': str(siteName), 
            "Type": "String", 
            "Valid": True 
        } 
        metric['code_name'] = {
            'value': '', 
            'Type': "String", 
            'Valid': False 
        } 
        metric['type_name'] = {
            'value': 'BETI CONTENEUR', 
            'Type': "String", 
            'Valid': True 
        } 
        metric['var_1'] = {
            'value': instance.main_alarm, 
            'Type': "Int64", 
            'Valid': True 
        } 
        metric['var_2'] = {
            'value': instance.door_contact_alarm, 
            'Type': "Int64", 
            'Valid': True 
        } 
        metric['var_3'] = {
            'value': instance.spd_alarm, 
            'Type': "Int64", 
            'Valid': True 
        } 
        metric['var_4'] = {
            'value': instance.ems_com_fail_alarm, 
            'Type': "Int64", 
            'Valid': True 
        } 
        metric['var_5'] = {
            'value': instance.gen_alarm, 
            'Type': "Int64", 
            'Valid': True 
        } 
        metric['var_6'] = {
            'value': instance.pload, 
            'Type': "Float64", 
            'Valid': True 
        } 
        metric['var_7'] = {
            'value': instance.pbat, 
            'Type': "Float64", 
            'Valid': True 
        } 
        metric['var_8'] = {
            'value': instance.psol, 
            'Type': "Float64", 
            'Valid': True 
        } 
        metric['var_9'] = {
            'value': instance.totalpower, 
            'Type': "Float64", 
            'Valid': True 
        } 
        metric['var_10'] = {
            'value': instance.soc, 
            'Type': "Float64", 
            'Valid': True 
        } 
        metric['var_11'] = {
            'value': instance.solar_logd, 
            'Type': "Int64", 
            'Valid': True 
        } 
        metric['var_12'] = {
            'value': instance.fuel_level, 
            'Type': "Float64", 
            'Valid': True 
        } 
        metric['var_13'] = {
            'value': instance.bei.fuel_capacity, 
            'Type': "Int64", 
            'Valid': True 
        } 
        metric['var_14'] = {
            'value': int((var_18 - datetime.now())/timedelta(hours=1)), 
            'Type': "Int64", 
            'Valid': True 
        } 
        metric['var_15'] = {
            'value': instance.bat_temp, 
            'Type': "Float64", 
            'Valid': True 
        } 
        metric['var_16'] = {
            'value': instance.ge_temp, 
            'Type': "Float64", 
            'Valid': True 
        } 
        metric['var_17'] = {
            'value': instance.ext_temp, 
            'Type': "Float64", 
            'Valid': True 
        } 
        metric['var_18'] = {
            'value': re.sub(' [\d\d:?]+$', '', str(var_18)), 
            'Type': "String", 
            'Valid': True 
        } 

        return metric 
     

class LocationSerializer(serializers.Serializer): 

    bei = BeiSerializer().context 
    site = SiteSerializer().context 
    install = InstallationSerializer().context 

    class Meta: 
        fields = () 

    def to_representation(self, instance): 
        datetime_installation = re.sub(' ', 'T', str(instance.installation_date)) 
        location = super().to_representation(instance) 
        location['id'] = instance.bei.id 
        location['type_name'] = {
            'value': str(instance.bei.serial_number), 
            'Type': "String", 
            'Valid': True 
        } 
        location['client'] = { 
            'value': instance.bei.client.name 
        } 
        location['first_running'] = {
            'value': re.sub('\+[\d\d:?]+$', '.00Z', str(datetime_installation)), 
            'Type': "Time", 
            'Valid': True 
        } 
        location['name'] = {
            'value': instance.site.name, 
            'Type': "String", 
            'Valid': True 
        } 
        location['long'] = {
            'value': instance.site.address.lng, 
            'Type': "String", 
            'Valid': True 
        } 
        location['lat'] = {
            'value': instance.site.address.lat, 
            'Type': "String", 
            'Valid': True 
        } 

        return location 

