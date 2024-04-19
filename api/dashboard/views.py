# models 
from dashboard.models import ( 
    Address, Bei, Client, Client_profile, 
    Installation, Maintenance, Site,  
) 
from data_acquisition.models import ( 
    Door_event, Data_acquisition 
) 
from django.contrib.auth.models import User 
# serializers 
from dashboard.serializers import ( 
    AddressSerializer, 
    ClientSerializer, 
    FileUploadSerializer, 
    InstallationSerializer, 
    LocationSerializer, 
    MaintenanceSerializer, 
    MetricSerializer, 
    SiteSerializer 
) 
# permissions 
from dashboard.permissions import IsAdminAuthenticated, IsOwnerGroup  # , IsManagerGroup 
from django.contrib.auth.hashers import make_password 
from dashboard.utils.parser import filter_last 
# utils 
import pandas as pd 
import csv 
from datetime import datetime 
from rest_framework import status 
from rest_framework.generics import CreateAPIView 
from rest_framework.parsers import MultiPartParser, JSONParser 

from rest_framework.permissions import IsAuthenticated 
from rest_framework.response import Response 
from rest_framework.views import APIView 
# Variables for the extend_schema decorator, OpenApiParameter.description : 
from dashboard.utils.query_params import locations, filter, last, from_, to 
# drf_spectacular 
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample 
from drf_spectacular.types import OpenApiTypes 



class Metrics(APIView): 
    # Authentication required 
    permission_classes = [IsAuthenticated, IsOwnerGroup,] 
    serializer_class = MetricSerializer 
    
    def get(self, request): 
        # Get the parameters: 
        mLocations = request.query_params.get('locations') 
        mFilter = request.query_params.get('filter') 
        mLast = request.query_params.get('last') 
        mFrom = request.query_params.get('from') 
        mTo = request.query_params.get('to') 
        
        # Prevent incompatibilities last+from and last+to: 
        if mLast != None: 
            if mFrom != None: 
                return Response('last and from are incompatibles') 
            elif mTo != None: 
                return Response('last and to are incompatibles') 

        metrics = [] 
        # Get current client: 
        user = User.objects.get(id=request.user.id) 
        client_user = Client_profile.objects.get( 
            client_user=user 
        ) 

        # /// metrics + locations params /// #         
        if mLocations != None: 
            beiList = Bei.objects.filter( 
                client=client_user.client, 
                id=mLocations 
            ) 
        else: 
            beiList = Bei.objects.filter( 
                client=client_user.client 
            ) 
        
        # Loop into the list of beis:  
        for bei in beiList: 
            # /// metrics + filter=duration + last params   /// # 
            if mFilter == 'duration': 
                if mLast == None: 
                    mLast = '1h' 
                
                targetLast = filter_last(mLast) 
            
                data_acquisitionList = Data_acquisition.objects.filter(
                    bei=bei, 
                    time__gte=targetLast 
                ).order_by('-time') 

            elif mFilter == 'time': 
                # /// metrics + filter=time + from + to params /// # 
                if mTo != None: 
                    # If param 'to' but no param 'from': 
                    # return all the beis until the 'to' date 
                    if mFrom == None: 
                        data_acquisitionList = Data_acquisition.objects.filter(
                            bei=bei, 
                            time__lte=mTo
                        ).order_by('bei', '-time') 

                    # If 'to' and 'from' 
                    data_acquisitionList = Data_acquisition.objects.filter( 
                        bei=bei, 
                        time__lte=mTo, time__gte=mFrom  
                    ).order_by('bei', '-time') 

                # /// metrics + filter=time + from /// # 
                elif mFrom != None: 
                    # If 'from' is in the future 
                    now = datetime.now() 
                    if mFrom > str(now): 
                        return Response('The date is in the future') 
                    
                    data_acquisitionList = Data_acquisition.objects.filter( 
                        bei=bei, 
                        time__gte=mFrom 
                    ).order_by('bei', '-time') 

            else: 
                if (mFilter == None) & (mFrom != None): 
                    return Response('"from" must be used with "filter=time"') 
                if (mFilter == None) & (mLast != None): 
                    return Response('"last" must be used with "filter=duration"') 
                
                data_acquisitionList = Data_acquisition.objects.filter( 
                    bei=bei 
                ).order_by('bei', '-time') 
        
            for data_acquisition in data_acquisitionList: 
                # Send the current bei to the serializer 
                serializer = MetricSerializer( 
                    data_acquisition, context={ 
                        'beiId': data_acquisition.bei 
                    }
                ) 
                metrics.append(serializer.data) 

        return Response(metrics) 


class Locations(APIView):

    # Authentication required 
    permission_classes = [IsAuthenticated, IsOwnerGroup, ] 
    serializer_class = LocationSerializer 

    
    def get(self, request): 

        locations = [] 

        # Get the entities 
        user = User.objects.get(id=request.user.id) 
        client_user = Client_profile.objects.get( 
            client_user=user 
        ) 
        beiList = Bei.objects.filter( 
            client=client_user.client 
        ) 

        # Loop into the registered beis 
        for registered_bei in beiList: 
            install = Installation.objects.get(bei=registered_bei) 
            # Send the installation for the current bei and client 
            serializer = LocationSerializer( 
                install, context={ 
                    'id': install.id, 
                    'bei': install.bei.serial_number, 
                    'client': install.bei.client.id 
                } 
            ) 
            locations.append(serializer.data) 

        return Response(locations) 


class NewClientView(CreateAPIView): 
    
    # Authentication required 
    permission_classes = [IsAdminAuthenticated,] 
    serializer_class = ClientSerializer 
    queryset = Client.objects.all() 


class NewBeiView(CreateAPIView): 
    """ 
        Creates a Bei instance without a CSV file. 
        Fill data for Address, Site, Bei and Installation. 
        Maintenance will be created by a signal. 
        
    """ 
    # Authentication required 
    permission_classes = [IsAdminAuthenticated,] 
    serializer_class = InstallationSerializer 
    parser_classes = [JSONParser] 

    def post(self, request, format=None): 
        """ 
            Send data for creation of: Address , Site, Bei and Installation instances, formated in JSON. Formate the data in 
            Args:
                request (dictionnary): contains the sent data in request.data (dictionnary) 
            Returns:
                Response : Status of the operation (201 if successfuly created) 
        """ 
        data = JSONParser().parse(request) 
        # Send the data to the serializer for validating 
        # and saving them in the DB 
        # serializer = InstallationSerializer(data=data_installation) 
        serializer = InstallationSerializer(data=data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201) 
        return Response(serializer.errors, status=400) 


class NewManyBeisView(CreateAPIView): 
    """ 
        Create Bei instances from CSV file. 
        Fill data for Address, Site, Bei and maintenance. 
        Installation will be created by a signal. 
    """ 

    # Authentication required 
    permission_classes = [IsAdminAuthenticated,] 
    serializer_class = FileUploadSerializer 
    parser_classes = [MultiPartParser] 

    def post(self, request, *args, **kwargs): 
        """ Send file with data for creation of Address, Site, Bei and Maintenance instances. 
        Args:
            request (Object): contains the sent file in request.data (dictionnary) 
        Returns:
            Response : Status of the operation (201 if successfuly created) 
        """ 
        serializer = self.get_serializer(data=request.data) 
        serializer.is_valid(raise_exception=True) 
        bei_file = serializer.validated_data['file'] 
        reader = pd.read_csv(bei_file) 
        beis = [] 
        for _, row in reader.iterrows(): 
            data = row 
            
            data_installation = { 
                "site": { 
                    "address": { 
                        "city": data['city'], 
                        "zipcode": data['zipcode'], 
                        "street": data['street'], 
                        "street_number": data['street_number'], 
                        "suplement": data['suplement'], 
                        "lat": data['lat'], 
                        "lng": data['lng'] 
                    }, 
                    "name": data['city'] 
                }, 
                "bei": { 
                    "serial_number": data['serial_number'], 
                    "fuel_capacity": data['fuel_capacity'], 
                    "client": { 
                        "name": data['client'], 
                        "password": "-" 
                    }, 
                    "password": make_password(data['password'])  
                }, 
                "installation_date": data['installation_date'] 
            } 
            beis.append(data_installation) 

        # Send the data to the serializer for validating 
        # and saving them in the DB 
        for bei in beis: 
            serializer = InstallationSerializer(data=bei) 
            if serializer.is_valid():
                serializer.save() 
            else: 
                return Response(serializer.errors, status=400) 
        return Response(serializer.data, status=201) 

    