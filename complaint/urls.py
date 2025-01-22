from django.urls import path
from .views import *

urlpatterns = [
    #students 
    path('create/', CreateComplaintAPIView.as_view(), name='create-complaint'), #for creating complains
    path('student/active/',ListStudentComplaintAPIView.as_view(), name='list-complaint'), #for listing all the active complaint 
    path('student/previous/',ListStudentPreviousComplaintAPIView.as_view(), name='list-previous-complaint'), #for listing all the resolved complaint 

    #supri
    path('supri/active/', ListAllComplaintAPIView.as_view(), name='list-all-complaints'),
    path('supri/previous/', ListAllPreviousComplaintAPIView.as_view(), name='list-all-previous-complaints'),
    path('supri/update-status/', UpdateComplaintStatusAPIView.as_view(), name='update-complaint-status'),  #its a put request
    path('supri/create-complaint/', CreateSupriComplaintAPIView.as_view(), name='supri-create-complaint'),

    #warden
    path('warden/all/', ListWardenComplaintsAPIView.as_view(), name='list-warden-complaints'),

    #EMS
    path('estate-manager/complaints/', EstateManagerComplaintsView.as_view(), name='estate-manager-complaints'),
    path('estate-manager/complaints/receipt/<str:serial_number>/', EstateManagerComplaintsView.as_view(), name='estate-manager-receipt'),


    #accessible to everyone who is authenticated
    path('resolve/<int:complaint_id>/', ResolveComplaintAPIView.as_view(), name='resolve-complaint'),
]