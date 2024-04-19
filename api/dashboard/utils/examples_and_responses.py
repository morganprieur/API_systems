# drf_spectacular 
from drf_spectacular.utils import OpenApiExample 


response_metrics = { 
    "timestamp": "2020-06-24 11:32:38.127805", 
    "id": {
        "Value": 1,
        "Type": "Int64",
        "Valid": True
    }, 
    "name": {
        "Value": "SITE_NAME_1",
        "Type": "String",
        "Valid": True
    },
    "code_name": {
        "Value": "CODE_NAME_1",
        "Type": "String",
        "Valid": False
    },
    "type_name": {
        "Value": "CONTENEUR",
        "Type": "String",
        "Valid": True
    },
    "var_1": {
        "Value": 0,
        "Type": "Int64",
        "Valid": True
    },
    "var_2": {
        "Value": 0,
        "Type": "Int64",
        "Valid": True
    },
    "var_3": {
        "Value": 0,
        "Type": "Int64",
        "Valid": True
    },
    "var_4": {
        "Value": 0,
        "Type": "Int64",
        "Valid": True
    },
    "var_5": {
        "Value": 1,
        "Type": "Int64",
        "Valid": True
    },
    "var_6": {
        "Value": 1556.1,
        "Type": "Float64",
        "Valid": True
    },
    "var_7": {
        "Value": -1556.1,
        "Type": "Float64",
        "Valid": True
    },
    "var_8": {
        "Value": 0,
        "Type": "Float64",
        "Valid": True
    },
    "var_9": {
        "Value": 0,
        "Type": "Float64",
        "Valid": True
    },
    "var_10": {
        "Value": 0.89,
        "Type": "Float64",
        "Valid": True
    },
    "var_11": {
        "Value": 3,
        "Type": "Int64",
        "Valid": True
    },
    "var_12": {
        "Value": 225,
        "Type": "Float64",
        "Valid": True
    },
    "var_13": {
        "Value": 0,
        "Type": "Int64",
        "Valid": False
    },
    "var_14": {
        "Value": 62277,
        "Type": "Int64",
        "Valid": True
    },
    "var_15": {
        "Value": 11,
        "Type": "Float64",
        "Valid": True
    },
    "var_16": {
        "Value": 19,
        "Type": "Float64",
        "Valid": True
    },
    "var_17": {
        "Value": 3,
        "Type": "Float64",
        "Valid": True
    },
    "var_18": {
        "Value": "2021-08-08",
        "Type": "String",
        "Valid": True
    } 
} 
expl_metrics = OpenApiExample( 
    name='metrics', 
    description='All metrics', 
    value=response_metrics 
) 
expl_metrics_locations = OpenApiExample( 
    name='metrics + locations', 
    description='Metrics for requested systems', 
    value=response_metrics
) 
expl_metrics_filter_last = OpenApiExample( 
    name='metrics + filter=duration + last=1h', 
    description='Metrics since last timelaps', 
    value=response_metrics 
) 
expl_metrics_filter_from = OpenApiExample( 
    name='metrics + filter=time + from=2022-11-01T01:02:03Z', 
    description='Metrics from datetime', 
    value=response_metrics 
) 
expl_metrics_filter_from_to = OpenApiExample( 
    name='metrics + filter=time + from=2022-11-01T01:02:03Z + to=2022-12-01T01:02:03Z', 
    description='Metrics from datetime and until datetime', 
    value=response_metrics 
) 

response_locations = { 
    "id": 1,
    "first_running": {
        "Value": "2022-11-24T00:00:00Z",
        "Type": "Time",
        "Valid": True
    },
    "long": {
        "Value": "5.366530",
        "Type": "String",
        "Valid": True
    },
    "lat": {
        "Value": "43.82583",
        "Type": "String",
        "Valid": True
    },
    "name": {
        "Value": "SITE_",
        "Type": "String",
        "Valid": True
    },
    "type_name": {
        "Value": "SYSTEM",
        "Type": "String",
        "Valid": True
    } 
} 
expl_locations = OpenApiExample( 
    name='locations', 
    summary='List all locations', 
    description='''List all locations available of client ''', 
    value=response_locations 
)

example_values_new_bei = OpenApiExample( 
    { 
        "installation": { 
            "site": { 
                "address": { 
                    "city": "Nimes1158", 
                    "zipcode": 30090, 
                    "street": "D418", 
                    "street_number": 0, 
                    "suplement": "", 
                    "lat": "43.8712644", 
                    "lng": "4.3277598" 
                }, 
                "name": "Nimes1158" 
            }, 
            "bei": { 
                "serial_number": "230110_1158", 
                "fuel_capacity": 300, 
                "client": { 
                    "name": "owner_01" 
                }, 
                "password": "pass" 
            }, 
            "installation_date": "2023-01-04T13:14:41.746Z"  
        } 
    } 
) 
response_new_bei = { 
    "installation": { 
        "site": { 
            "address": { 
                "city": "Nimes1158", 
                "zipcode": 30090, 
                "street": "D418", 
                "street_number": 1, 
                "suplement": "", 
                "lat": "43.8712644", 
                "lng": "4.3277598"
            }, 
            "name": "Nimes1158" 
        }, 
        "bei": { 
            "serial_number": "230110_1158", 
            "fuel_capacity": 300, 
            "client": { 
                "name": "owner_01" 
            }, 
            "password": "pass" 
        }, 
        "installation_date": "2023-01-04T13:14:41.746Z"  
    } 
} 

example_values_new_many_beis = OpenApiExample( 
    "serial_number,fuel_capacity,client,password,city,zipcode,street,street_number,suplement,lat,lng,installation_date\n"
    "230110_1134,300,1,pass_bei1134,Nimes1134,30090,chemin des sources,257,,43.8712644,4.3277598,2023-01-04T13:14:40.746Z\n"
    "230110_1135,300,2,pass_bei1135,Nimes1135,30090,chemin de la côte,2345,,43.8712644,4.3277598,2023-01-04T13:14:41.746Z\n" 
) 
response_new_many_beis = [ 
    { 
        "installation": { 
            "site": { 
                "address": { 
                    "city": "Nimes1158", 
                    "zipcode": 30090, 
                    "street": "D418", 
                    "street_number": 2, 
                    "suplement": "", 
                    "lat": "43.8712644", 
                    "lng": "4.3277598"
                }, 
                "name": "Nimes1158" 
            }, 
            "bei": { 
                "serial_number": "230110_1158", 
                "fuel_capacity": 300, 
                "client": { 
                    "name": "owner_01" 
                }, 
                "password": "pass" 
            }, 
            "installation_date": "2023-01-04T13:14:41.746Z"  
        } 
    } 
]  


example_data_acquisitions = '''{{ 
    "time": "2022-09-26 07:15:20", 
    "bei": 1, 
    "bat_temp": 2, 
    "solar_logd": 3, 
    "spd_alarm": 4, 
    "gen_alarm": 5, 
    "totalpower": 6, 
    "fuel_level": 7, 
    "ext_temp": 8, 
    "ge_temp": 9, 
    "soc": 10, 
    "main_alarm": 11, 
    "ems_com_fail_alarm": 12, 
    "door_contact_alarm": 13, 
    "pbat": 14, 
    "psol": 15, 
    "pload": 16
   
}} 
''' 
example_door_event = '''{{
    "bei":"1", 
    "state":"1"
}} 
'''

