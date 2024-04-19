""" bei URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
""" 
# from dashboard import urls as dashboard_urls
from dashboard import views as dashboard_views 
from data_acquisition import views as data_acquisition_views 

from django.contrib import admin 
from django.urls import include, path, re_path 
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, 
) 
from rest_framework import permissions 
# drf_spectacular 
from drf_spectacular.views import ( 
    SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView, 
) 



urlpatterns = [ 
    # Doc: drf_spectacular (dl YAML file) 
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Doc: UI: 
    path('api/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'), 

    # admin web interface 
    path('admin/', admin.site.urls), 

    # JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), 
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api-auth/', include('rest_framework.urls')), 

    # admin CLI 
    path('api/new_client/', dashboard_views.NewClientView.as_view(), name='new_client'), 
    # send data with a form : 
    path('api/new_bei/', dashboard_views.NewBeiView.as_view(), name='new_bei'), 
    # send a CSV file : 
    path('api/new_many_beis/', dashboard_views.NewManyBeisView.as_view(), name='new_beis'), 

    # application dashboard (GET) 
    path('api/metrics/', dashboard_views.Metrics.as_view(), name='metrics'), 
    path('api/locations/', dashboard_views.Locations.as_view(), name='locations'), 

    # application data_acquisition (POST) 
    path('api/new_data_acquisition/', data_acquisition_views.NewData_acquisitionView.as_view(), name='data_acquisition'), 
    path('api/new_door_event/', data_acquisition_views.NewDoor_eventView.as_view()), 
] 


