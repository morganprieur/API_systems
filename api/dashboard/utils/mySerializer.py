import re 


class MySerializer:

    @staticmethod
    def serializerDataLocation( 
        beiId, installation_date, siteName, lat, lng, beiName 
    ): 
        datetime_installation = re.sub(' ', 'T', str(installation_date))
    
        locationJson = {
            'id': str(beiId), 
            'first_running': { 
                'value': re.sub('\+[\d\d:?]+$', '.00Z', str(datetime_installation)), 
                'Type': "Time",
                'Valid': True
            }, 
            'long': {
                'Value': str(lng),
                'Type': "String",
                'Valid': True
            }, 
            'lat': {
                'Value': str(lat),
                'Type': "String",
                'Valid': True
            }, 
            'name': {
                'Value': str(siteName),
                'Type': "String",
                'Valid': True
            }, 
            'type_name':{
                'Value': str(beiName),
                'Type': "String",
                'Valid': True
            } 
        } 
        
        return locationJson
    

    @staticmethod 
    def serializerDataMetric(timestamp, id, name, code_name, type_name, var_1, 
        var_2, var_3, var_4, var_5, var_6, var_7, var_8, var_9, var_10, var_11, 
        var_12, var_13, var_14, var_15, var_16, var_17, var_18 
    ): 

        # ==== # "2022-09-27 07:15:20" 
        dt_data_acquisition = re.sub(str(timestamp), f'{timestamp}.000000', str(timestamp)) 
    
        metricsJson = { 
            'timestamp': str(dt_data_acquisition), 
            'id': {
                "Value": id,
                "Type": "Int64",
                "Valid": True
            }, 
            'name': {
                "Value": str(name),
                "Type": "String",
                "Valid": True 
            }, 
            'code_name': {
                "Value": str(code_name),
                "Type": "String",
                "Valid": False
            }, 
            'type_name': {
                "Value": str(type_name),
                "Type": "String",
                "Valid": True
            }, 
            'var_1': {
                "Value": var_1,
                "Type": "Int64",
                "Valid": True
            }, 
            'var_2': {
                "Value": var_2,
                "Type": "Int64",
                "Valid": True
            }, 
            'var_3': {
                "Value": var_3,
                "Type": "Int64",
                "Valid": True
            }, 
            'var_4': {
                "Value": var_4,
                "Type": "Int64",
                "Valid": True
            }, 
            'var_5': {
                "Value": var_5,
                "Type": "Int64",
                "Valid": True
            }, 
            'var_6': {
                "Value": var_6,
                "Type": "Float64",
                "Valid": True
            }, 
            'var_7': {
                "Value": var_7,
                "Type": "Float64",
                "Valid": True
            }, 
            'var_8': {
                "Value": var_8,
                "Type": "Float64",
                "Valid": True
            }, 
            'var_9': {
                "Value": var_9,
                "Type": "Float64",
                "Valid": True
            }, 
            'var_10': {
                "Value": var_10,
                "Type": "Float64",
                "Valid": True
            }, 
            'var_11': {
                "Value": var_11,
                "Type": "Int64",
                "Valid": True
            }, 
            'var_12': {
                "Value": var_12,
                "Type": "Float64",
                "Valid": True
            }, 
            'var_13': {
                "Value": var_13,
                "Type": "Int64",
                "Valid": False
            }, 
            'var_14': {
                "Value": var_14,
                "Type": "Int64",
                "Valid": True
            }, 
            'var_15': {
                "Value": var_15,
                "Type": "Float64",
                "Valid": True
            }, 
            'var_16': {
                "Value": var_16,
                "Type": "Float64",
                "Valid": True
            }, 
            'var_17': {
                "Value": var_17,
                "Type": "Float64",
                "Valid": True
            }, 
            'var_18': {
                "value": re.sub(' [\d\d:?]+$', '', str(var_18)),    # "2023-03-23 00:00:00" 
                "Type": "String",
                "Valid": True
            } 
        } 

        return metricsJson 

