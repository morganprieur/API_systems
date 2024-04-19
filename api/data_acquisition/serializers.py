
from data_acquisition.models import ( 
    Data_acquisition, Door_event 
) 
from dashboard.models import Bei, Bei_profile 
from django.contrib.auth.models import User 
from rest_framework import serializers 



class UserSerializer(serializers.ModelSerializer): 

    class Meta: 
        model = User 
        fields = [ 
            'id', 
            'username', 
            'groups' 
        ] 

class Bei_profileSerializer(serializers.ModelSerializer): 

    class Meta: 
        model = Bei_profile 
        fields = [ 
            'bei_user', 
            'bei' 
        ] 

class BeiSerializer(serializers.ModelSerializer): 

    class Meta: 
        model = Bei 
        fields = [ 
            'id', 
            'serial_number', 
            'fuel_capacity', 
            'client' 
        ] 


class Data_acquisitionSerializer(serializers.ModelSerializer): 

    time = serializers.DateTimeField( 
        required=True 
    ) 
    bat_temp = serializers.IntegerField() 
    solar_logd = serializers.IntegerField() 
    spd_alarm = serializers.IntegerField() 
    gen_alarm = serializers.IntegerField() 
    totalpower = serializers.FloatField() 
    fuel_level = serializers.FloatField() 
    ext_temp = serializers.IntegerField() 
    ge_temp = serializers.IntegerField() 
    soc = serializers.FloatField() 
    main_alarm = serializers.IntegerField() 
    ems_com_fail_alarm = serializers.IntegerField() 
    door_contact_alarm = serializers.IntegerField() 
    pbat = serializers.FloatField() 
    psol = serializers.FloatField() 
    pload = serializers.FloatField() 

    class Meta: 
        model = Data_acquisition 
        fields = [ 
            'time', 'bei', 'bat_temp', 'solar_logd', 'spd_alarm', 'gen_alarm', 
            'totalpower', 'fuel_level', 'ext_temp', 'ge_temp', 'soc', 'main_alarm', 
            'ems_com_fail_alarm', 'door_contact_alarm', 'pbat', 'psol', 'pload' 
        ] 

    def create(self, validated_data):
        """
        Create and return a new data_acquisition instance, given the validated data.
        """
        return Data_acquisition.objects.create(**validated_data) 


class Door_eventSerializer(serializers.ModelSerializer): 

    class Meta: 
        model = Door_event 
        fields = [ 
            'time', 'bei', 'state' 
        ] 

    def create(self, validated_data):
        """
        Create and return a new data_acquisition instance, given the validated data.
        """
        return Door_event.objects.create(**validated_data) 



