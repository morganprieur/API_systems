# drf_spectacular 
from drf_spectacular.utils import OpenApiParameter 


locations = OpenApiParameter( 
    name='locations', 
    description='''Example:"1, 2" \nFilter locations by id.''', 
    required=False, 
    type=str 
) 
filter = OpenApiParameter( 
    name='filter', 
    description='''Filter by duration or datetime \n
        Values: "filter=duration&last=1h", or "filter=time&from=datetime" or "filter=time&from=datetime&to=datetime" \n
        Default: "filter=duration&last=1h". ''', 
    required=False, 
    type=str 
) 
last = OpenApiParameter( 
    name='last', 
    description='''"filter=duration" [0-9hdm] \n
        Default: "1h" \n
        Example: "filter=duration&last=1h" \n
        Duration in minutes, hours, days (e.g. : 10m, 1h, 24h). \n
        Must be used together with filter. \n
        This parameter is incompatible with from. ''', 
    required=False, 
    type=str 
) 
from_ = OpenApiParameter( 
    name='from', 
    description='''"date-time" \n
        Example: "from=2022-11-01T01:02:03Z" \n
        Returns metrics from point in time (ISO8601 format). \n
        Must be used together with filter. \n
        This parameter is incompatible with last.' ''' , 
    required=False, 
    type=str 
) 
to = OpenApiParameter( 
    name='to', 
    description='''"date-time" \n
        Example:"from=2022-11-01T01:02:03Z&to=2022-13-01T01:02:03Z" \n
        Returns metrics until point in time (ISO8601 format). \n
        Must be used together with filter. \n
        This parameter is incompatible with last. ''' , 
    required=False, 
    type=str 
) 
 

