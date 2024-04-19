from django.db import models 
from dashboard.models import Bei 


class Door_event(models.Model): 
    time = models.DateTimeField(
        primary_key = True, 
        auto_now_add = True
    )
    bei = models.ForeignKey(
        Bei, 
        on_delete = models.CASCADE, 
        related_name = 'door_event_bei' 
    ) 
    state = models.SmallIntegerField()

    def __str__(self): 
        return f'{self.time}'


class Data_acquisition(models.Model):
    """ Table to split in many tables """
    time = models.DateTimeField( 
        primary_key = True,
        auto_now_add = True
    )
    bei = models.ForeignKey(
        Bei,
        on_delete = models.CASCADE, 
        related_name = 'data_acquisition_bei' 
    ) 
    bat_temp = models.IntegerField() 

    solar_logd = models.IntegerField() 
    spd_alarm = models.IntegerField() 
    gen_alarm = models.IntegerField() 
    totalpower = models.FloatField() 
    fuel_level = models.FloatField() 
    ext_temp = models.IntegerField() 
    ge_temp = models.IntegerField() 
    soc = models.FloatField() 
    main_alarm = models.IntegerField()
    ems_com_fail_alarm = models.IntegerField() 
    door_contact_alarm = models.IntegerField() 
    pbat = models.FloatField() 
    psol = models.FloatField() 
    pload = models.FloatField() 


    def __str__(self): 
        return f'{self.time}'  


