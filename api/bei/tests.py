from dashboard.models import (
    Client, Bei, Address, Site, Installation, Maintenance, 
) 
from data_acquisition.models import ( 
    Door_event, Data_acquisition 
) 

from django.contrib.auth.models import User, Group 
from django.test import TestCase 

from datetime import timedelta 
import re 


class ClientModelTests(TestCase): 
    """ Tests of data contents and formats """ 

    @classmethod 
    def setUpTestData(cls): 

        # Setup 2 groups 
        cls.grp_owner = Group.objects.create(name='owner_group') 
        cls.grp_bei = Group.objects.create(name='bei_group') 
        cls.groups = Group.objects.all() 
        # print('groups ln 18 : ', cls.groups) 


        # Setup data for tests : 2 clients, 2 beis each, 2 datasets by bei 
        numbers_of_entities = {
            'clients': 2, 
            'beis': 4, 
            'addresses': 4, 
            'sites': 4, 
            'installations': 4, 
            'maintenances': 4, 
            'door_events': 8, 
            'data_acquisitions': 8 
        } 

        # 2 new clients 
        for client_id in range(numbers_of_entities['clients']): 
            cls.client = Client.objects.create(name=f'Client_0{client_id+1}') 


        # 2 beis by client 
        for bei_id in range(numbers_of_entities['beis']): 
            b = bei_id+1 
            if b <=2: 
                client = Client.objects.get(pk=b) 
            else: 
                client = Client.objects.get(pk=b-2) 

            cls.bei = Bei.objects.create( 
                serial_number=f'Bei_0{b}', 
                client=client, 
                fuel_capacity=300
            ) 
        
        cls.beis = Bei.objects.all() 


        # 4 Addresses 
        for address_id in range(numbers_of_entities['addresses']): 
            cls.address = Address.objects.create(
                city = f'Address_0{address_id+1}', 
                zipcode = f'3800{address_id}', 
                street = f'rue {address_id}', 
                street_number = f'10{address_id}', 
                lat = 45.6478152, 
                lng = 5.1035071 
            ) 


        # 4 sites 
        for site_id in range(numbers_of_entities['sites']): 
            addr = Address.objects.get(pk=site_id+1) 
            cls.site = Site.objects.create(
                name = addr.city, 
                address = addr 
            ) 
        

        # Installations 
        for installation_id in range(numbers_of_entities['installations']): 
            inst = installation_id+1 
            site = Site.objects.get(pk=inst) 
            bei = Bei.objects.get(pk=inst) 
            cls.installation = Installation.objects.create(
                site = site, 
                bei = bei, 
                installation_date = '2022-09-21 07:15:20' 
            ) 


        # Maintenances 
        for maintenance_id in range(numbers_of_entities['maintenances']): 
            bei = Bei.objects.get(pk=maintenance_id+1) 
            cls.maintenance = Maintenance.objects.create(
                bei = bei, 
                description = 'Démarrage après installation', 
                maintenance_name = f'Démarrage {bei.serial_number}', 
                maintenance_date = '2022-09-21 07:15:20' 
            ) 


        # Door_events 
        for bei in cls.beis: 
            cls.door_event = Door_event.objects.create(
                bei=bei,
                state=1 
            ) 


        # Data_acquisitions 
        for bei in cls.beis: 
            cls.data_acquisition = Data_acquisition.objects.create(
                bei=bei,
                main_alarm=111,     # var_1 
                door_contact_alarm=222,     # var_2 
                spd_alarm=333,     # var_3 
                ems_com_fail_alarm=444,     # var_4 
                gen_alarm=555,     # var_5 
                pload=666,     # var_6 
                pbat=777,     # var_7 
                psol=888,     # var_8 
                totalpower=999,     # var_9 
                soc=111,   # var_10 
                solar_logd=212,     # var_11 
                fuel_level=313,     # var_12 
                bat_temp=70,     # var_15 
                ge_temp=50,     # var_16 
                ext_temp=18     # var_17 
            ) 


    def test_clients(cls): 
        """ Tests the creation of 2 clients """ 

        cls.clients = Client.objects.all() 
        cls.last_client = Client.objects.last() 

        n = 0 
        for client in cls.clients: 
            n += 1 
        
            cls.assertEquals(client.id, n) 
            cls.assertEquals(client.name, f'Client_0{n}') 
        
        cls.assertEquals(cls.last_client.id, 2) 

    
    def test_client_users_created_by_signal(cls): 
        """ tests the creation of users associated with the clients """ 

        cls.users = User.objects.all() 

        n = 0 
        for user in cls.users: 
            n += 1 

            if user.username.startswith('cli_'): 
                cls.assertEquals(user.id, n) 
                cls.assertEquals(user.username, f'cli_Client_0{n}') 
        

    def test_beis_and_bei_users_created_by_signal(cls): 
        """ tests the creation of beis and users associated with the beis """ 
        
        cls.last_bei = Bei.objects.last() 
        cls.beis = Bei.objects.all() 

        n = 0 
        for bei in cls.beis: 
            n += 1 
            cls.assertEquals(bei.id, n) 
            cls.assertEquals(bei.serial_number, f'Bei_0{n}') 
            if bei.id%2!=0: 
                cls.assertEquals(bei.client.id, 1) 
            else: 
                cls.assertEquals(bei.client.id, 2) 

        # tests users et bei users 
        cls.users = User.objects.all() 
        n = 0 
        for user in cls.users: 
            n += 1 
            cls.assertEquals(user.id, n) 
            if user.username.startswith('bei_'): 
                cls.assertEquals(user.username, f'bei_Bei_0{n-2}') 
        cls.last_user = User.objects.last() 
        cls.assertEquals(cls.last_user.username, 'bei_Bei_04') 


    def test_addresses(cls): 
        """ tests the creation of addresses """ 

        cls.addresses = Address.objects.all() 
        cls.last_address = Address.objects.last() 

        n = 0 
        for address in cls.addresses: 
            n += 1 

            cls.assertEquals(address.id, n) 
            cls.assertEquals(address.city, f'Address_0{address.id}') 


    def test_sites(cls): 
        """ tests the creation of sites associated with the addresses """ 

        cls.sites = Site.objects.all() 
        cls.last_site = Site.objects.last() 

        n = 0 
        for site in cls.sites: 
            n += 1 

            cls.assertEquals(site.id, n) 
            cls.assertEquals(site.name, f'Address_0{n}') 
            cls.assertEquals(site.address, Address.objects.get(pk=n)) 


    def test_installations(cls): 
        """ tests the creation of installations associated with the beis and sites """ 

        cls.installations = Installation.objects.all() 
        cls.last_installation = Installation.objects.last() 

        n = 0 
        for installation in cls.installations: 
            n += 1 

            cls.assertEquals(installation.id, n) 
            cls.assertEquals(installation.site.name, f'Address_0{n}') 
            cls.assertEquals(installation.bei.serial_number, f'Bei_0{n}') 

            datetime_installation = re.sub(' ', 'T', str(installation.installation_date)) 
            dtime = re.sub('\+[\d\d:?]+$', '.00Z', str(datetime_installation)) 

            cls.assertRegex(str(dtime), '^\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\d.\d\dZ')   #  "2022-09-21T07:15:20.00Z" 


    def test_maintenances(cls): 
        """ tests the creation of maintenances associated with the beis """ 

        cls.maintenances = Maintenance.objects.all() 
        cls.last_maintenance = Maintenance.objects.last() 

        n = 0 
        for maintenance in cls.maintenances: 
            n += 1 

            cls.assertEquals(maintenance.id, n) 
            cls.assertEquals(maintenance.maintenance_name, f'Démarrage Bei_0{n}') 

            # Date de prochaine maintenance de la BETI 
            deltaMaintenance_date = timedelta(days=366/2) 
            datetime_proch_maintenance_tz_none = (maintenance.maintenance_date + deltaMaintenance_date).replace(tzinfo=None) 
            maintenance_date_seule = re.sub(' [\d\d:?]+$', '', str(datetime_proch_maintenance_tz_none)) 
            cls.assertRegex(str(maintenance_date_seule), '^\d\d\d\d-\d\d-\d\d')   #  "2022-10-14")) 


    def test_door_events(cls): 
        """ tests the creation of door_events associated with the beis """ 

        cls.door_events = Door_event.objects.all() 
        cls.last_door_event = Door_event.objects.last() 

        n = 0 
        for door_event in cls.door_events: 
            n += 1 

            if n <= 4: 
                cls.assertEquals(door_event.bei.serial_number, f'Bei_0{n}') 
            else: 
                cls.assertEquals(door_event.bei.serial_number, f'Bei_0{n-4}') 

            dtime = (door_event.time).replace(tzinfo=None) 
            cls.assertRegex(str(dtime), '^\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d.\d\d\d\d\d\d') 


    def test_data_acquisitions(cls): 
        """ tests the creation of data_acquisitions associated with the beis """ 

        cls.data_acquisitions = Data_acquisition.objects.all() 

        n = 0 
        for data_acquisition in cls.data_acquisitions: 
            n += 1  

            if n <= 4: 
                cls.assertEquals(data_acquisition.bei.serial_number, f'Bei_0{n}') 
            else: 
                cls.assertEquals(data_acquisition.bei.serial_number, f'Bei_0{n-4}') 
            
            dtime = (data_acquisition.time).replace(tzinfo=None) 
            cls.assertRegex(str(dtime), '^\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d.\d\d\d\d\d\d')   #  "2022-10-14 11:32:38.127805")) 
            cls.assertEquals(data_acquisition.main_alarm, 111) 
            cls.assertEquals(str(type(data_acquisition.main_alarm)), "<class 'int'>") 
            cls.assertEquals(data_acquisition.door_contact_alarm, 222) 
            cls.assertEquals(str(type(data_acquisition.door_contact_alarm)), "<class 'int'>") 
            cls.assertEquals(data_acquisition.spd_alarm, 333) 
            cls.assertEquals(str(type(data_acquisition.spd_alarm)), "<class 'int'>") 
            cls.assertEquals(data_acquisition.ems_com_fail_alarm, 444) 
            cls.assertEquals(str(type(data_acquisition.ems_com_fail_alarm)), "<class 'int'>") 
            cls.assertEquals(data_acquisition.gen_alarm, 555) 
            cls.assertEquals(str(type(data_acquisition.gen_alarm)), "<class 'int'>") 
            cls.assertEquals(data_acquisition.pload, 666) 
            cls.assertEquals(str(type(data_acquisition.pload)), "<class 'float'>") 
            cls.assertEquals(data_acquisition.pbat, 777) 
            cls.assertEquals(str(type(data_acquisition.pbat)), "<class 'float'>") 
            cls.assertEquals(data_acquisition.psol, 888) 
            cls.assertEquals(str(type(data_acquisition.psol)), "<class 'float'>") 
            cls.assertEquals(data_acquisition.totalpower, 999) 
            cls.assertEquals(str(type(data_acquisition.totalpower)), "<class 'float'>") 
            cls.assertEquals(data_acquisition.soc, 111) 
            cls.assertEquals(str(type(data_acquisition.soc)), "<class 'float'>") 
            cls.assertEquals(data_acquisition.solar_logd, 212) 
            cls.assertEquals(str(type(data_acquisition.solar_logd)), "<class 'int'>") 
            cls.assertEquals(data_acquisition.fuel_level, 313) 
            cls.assertEquals(str(type(data_acquisition.fuel_level)), "<class 'float'>") 
            cls.assertEquals(data_acquisition.bat_temp, 70) 
            cls.assertEquals(str(type(data_acquisition.bat_temp)), "<class 'int'>") 
            cls.assertEquals(data_acquisition.ge_temp, 50) 
            cls.assertEquals(str(type(data_acquisition.ge_temp)), "<class 'int'>") 
            cls.assertEquals(data_acquisition.ext_temp, 18) 
            cls.assertEquals(str(type(data_acquisition.ext_temp)), "<class 'int'>") 

