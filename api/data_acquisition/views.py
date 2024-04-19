# models 
from data_acquisition.models import Door_event, Data_acquisition 
from dashboard.models import Bei, Bei_profile 
from django.contrib.auth.models import User 
# serializers 
from data_acquisition.serializers import ( 
    Door_eventSerializer, Data_acquisitionSerializer 
) 
# permissions 
from dashboard.permissions import IsAdminAuthenticated 
from data_acquisition.permissions import IsBeiGroup 
from rest_framework.permissions import IsAuthenticated 
# utils 
from datetime import datetime 
from rest_framework import status 
from rest_framework.generics import CreateAPIView 
from rest_framework.response import Response 
from rest_framework.views import APIView 


class NewDoor_eventView(APIView): 

    # Authentication required 
    permission_classes = [IsAuthenticated, IsBeiGroup, ] 

    def post(self, request, **kwargs):  
        """Creates a door_event dataset for the connected bei_user to regsiter in the DB. 
        Args:
            request (request): contains the data to register and the connected user object. 
        """ 
        if request.method == 'POST': 
            user = User.objects.get(id=request.user.id) 
            bei_user = Bei_profile.objects.get(bei_user=user) 
            connected_bei = bei_user.bei 
            bei = Bei.objects.get(id=connected_bei.id) 

            data = request.data 
            data['time'] = datetime.now() 
            data['bei']  = bei.id 

            serializer = Door_eventSerializer(data=data) 
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400) 


class NewData_acquisitionView(CreateAPIView): 
    # Authentication required 
    permission_classes = [IsAuthenticated, IsBeiGroup, ] 
    serializer_class = Data_acquisitionSerializer 

    def post(self, request, **kwargs): 
        """ Creates a data_acquisition dataset for the connected bei_user to regsiter in the DB. 
        Args:
            request (request): contains the data to register and the connected user object. 
        """ 
        if request.method == 'POST': 
            
            user = User.objects.get(id=request.user.id) 
            bei_user = Bei_profile.objects.get(bei_user=user) 
            connected_bei = bei_user.bei 
            bei = Bei.objects.get(id=connected_bei.id) 

            data = request.data 
            data['time'] = datetime.now() 
            data['bei']  = bei.id 

            serializer = Data_acquisitionSerializer(data=data) 
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400) 

