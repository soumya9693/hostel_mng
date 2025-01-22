from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import BhavanComplaints
from django.db import models
from .serializers import BhavanComplaintsSerializer, WardenComplaintsSerializer, EstateManagerComplaintSerializer
from users.permissions import IsSuperintendent, IsEstateManager, IsWarden, IsStudent



#create complaint for student 
class CreateComplaintAPIView(APIView):
    permission_classes = [IsStudent]

    def post(self, request):
        """
        some fields are otional check serializer just in case student wants to complain only about toilet and stuff 
        Expected request data:

        {
            "block": "0",
            "floor": "1",
            "room_number": "101",
            "toilet": "T1",
            "request_related": "Carpenter",
            "subcategory": "Door",
            "complaint_description": "Door hinge is broken"
        }
        """
        request.data['user'] = request.user.id
        serializer = BhavanComplaintsSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'message': 'Complaint submitted successfully', 
                    'complaint_data': serializer.data
                }, 
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                'message': 'Invalid complaint data', 
                'errors': serializer.errors
            }, 
            status=status.HTTP_400_BAD_REQUEST
        )

#list all the complaint for a given student which are active 
#the approved and To EMS should reflect in progress on frontend according to UI
class ListStudentComplaintAPIView(APIView):
    """
    Lists all active complaints (Pending, Approved, In_progress) for the current student
    
    Permissions:
        - User must be a student
    
    Response:
    {
        "message": "Active complaints retrieved successfully",
        "complaints": [
            {
                "id": 1,
                "user": 1,
                "block": "0",
                "floor": "1",
                "room_number": "101",
                "toilet": "T1",
                "request_related": "Carpenter",
                "subcategory": "Door",
                "complaint_description": "Door hinge is broken",
                "complaint_status": "Pending",
                "reported_at": "2024-01-01T10:00:00Z"
            },
            ...
        ]
    }
    """
    permission_classes = [IsStudent]

    def get(self, request):
        user = request.user
        active_statuses = ['Pending', 'Approved','In_progress']
        complaints = BhavanComplaints.objects.filter(
            user=user,
            complaint_status__in=active_statuses
        ).order_by('-reported_at') #sending in decending order 
        
        serializer = BhavanComplaintsSerializer(complaints, many=True)
        return Response({
            'message': 'Active complaints retrieved successfully yayyy',
            'complaints': serializer.data
        })

#for previous complaint by student which are resolved
class ListStudentPreviousComplaintAPIView(APIView):
    """
    Lists all resolved complaints for the current user
    
    Permissions:
        - User must be a student
    
    Response:
    {
        "message": "Previous complaints retrieved successfully",
        "complaints": [
            {
                "id": 1,
                "user": 1,
                "block": "0",
                "floor": "1",
                "room_number": "101",
                "toilet": "T1",
                "request_related": "Carpenter",
                "subcategory": "Door",
                "complaint_description": "Door hinge is broken",
                "complaint_status": "Resolved",
                "reported_at": "2024-01-01T10:00:00Z"
            },
            ...
        ]
    }
    """
    permission_classes = [IsStudent]

    def get(self, request):
        user = request.user
        complaints = BhavanComplaints.objects.filter(
            user=user,
            complaint_status='Resolved'
        ).order_by('-reported_at')
        
        serializer = BhavanComplaintsSerializer(complaints, many=True)
        return Response({
            'message': 'Previous complaints retrieved successfully',
            'complaints': serializer.data
        })



#supri apis 

class UpdateComplaintStatusAPIView(APIView):
    """
    Updates the status of a complaint. Only accessible by Superintendent.
    Allowed transitions:
    - Pending → Approved
    - Approved → Pending 
    - when sent_toEMS=True → Status automatically set to In_progress
    
    Permissions:
        - User must be a Superintendent
    
    Request:
    {
        "complaint_id": 1,
        "new_status": "Approved",
        "send_to_ems": true  # optional boolean field for send to ems button  
    }
    
    Response:
    {
        "message": "Complaint status updated successfully",
        "complaint": {
            "id": 1,
            "user": 1,
            "block": "0",
            "floor": "1",
            "room_number": "101",
            "toilet": "T1",
            "request_related": "Carpenter",
            "subcategory": "Door",
            "complaint_description": "Door hinge is broken",
            "complaint_status": "Approved",
            "sent_toEMS": true,
            "reported_at": "2024-01-01T10:00:00Z"
        }
    }
    
    Error Response:
    {
        "message": "Error message",
        "errors": {
            "detail": "Specific error details"
        }
    }
    """
    permission_classes = [IsSuperintendent]

    def _is_valid_transition(self, current_status, new_status):
        valid_transitions = {
            'Pending': ['Approved'],
            'Approved': ['Pending']
        }
        
        return current_status in valid_transitions and new_status in valid_transitions[current_status]

    def put(self, request):

        complaint_id = request.data.get('complaint_id')
        if not complaint_id:
            return Response({
                'message': 'Missing required field',
                'errors': {'detail': 'complaint_id is required'}
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            complaint = BhavanComplaints.objects.get(id=complaint_id)
        except BhavanComplaints.DoesNotExist:
            return Response({
                'message': 'Complaint not found',
                'errors': {'detail': f'No complaint found with id {complaint_id}'}
            }, status=status.HTTP_404_NOT_FOUND)

        new_status = request.data.get('new_status')
        valid_new_statuses = ['Approved', 'Pending']
        if not new_status or new_status not in valid_new_statuses:
            return Response({
                'message': 'Invalid status value',
                'errors': {'detail': f'Status must be one of: {", ".join(valid_new_statuses)}'}
            }, status=status.HTTP_400_BAD_REQUEST)

        current_status = complaint.complaint_status
        if not self._is_valid_transition(current_status, new_status):
            valid_transitions = {
                'Pending': ['Approved'],
                'Approved': ['Pending']
            }
            valid_next_states = valid_transitions.get(current_status, [])
            return Response({
                'message': 'Invalid status transition',
                'errors': {
                    'detail': f'Cannot transition from {current_status} to {new_status}. '
                            f'Valid next states are: {", ".join(valid_next_states)}'
                }
            }, status=status.HTTP_400_BAD_REQUEST)

    
        try:
            
            send_to_ems = request.data.get('send_to_ems', False)
            
            if send_to_ems:
                complaint.complaint_status = 'In_progress'
                complaint.sent_toEMS = True
            else:
                complaint.complaint_status = new_status
                complaint.sent_toEMS = False
            complaint.save()

        except Exception as e:
            return Response({
                'message': 'Error updating complaint',
                'errors': {'detail': str(e)}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
        try:
            serializer = BhavanComplaintsSerializer(complaint)
            return Response({
                'message': 'Complaint updated successfully',
                'details': {
                    'previous_status': current_status,
                    'new_status': complaint.complaint_status,
                    'sent_to_ems': complaint.sent_toEMS
                },
                'complaint': serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'message': 'Error serializing complaint data',
                'errors': {'detail': str(e)}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def get(self, request):
        """
        Get the valid status transitions for reference
        """
        valid_transitions = {
            'Pending': ['Approved','send_to_ems: False' ],
            'pending': ['Approved', 'send_to_ems: True sets the status to in progress'],
            'Approved': ['Pending'] #just in case supri decides to take revenge on a student 
        }
        
        return Response({
            'message': 'Valid status transitions',
            'transitions': valid_transitions
        })

#create complaint for supri
class CreateSupriComplaintAPIView(APIView):
    """
    API endpoint for Superintendent to create complaints directly.
    All complaints created by Superintendent are automatically marked as sent to EMS.
    
    Permissions:
        - User must be a Superintendent
    
    Expected request data:
    {
        "block": "0",
        "floor": "1",
        "room_number": "101",
        "toilet": "T1",
        "request_related": "Carpenter",
        "subcategory": "Door",
        "complaint_description": "Door hinge is broken"
    }
    
    Response:
    {
        "message": "Complaint created successfully",
        "complaint_data": {
            "id": 1,
            "user": 5,  
            "block": "0",
            "floor": "1",
            "room_number": "101",
            "toilet": "T1",
            "request_related": "Carpenter",
            "subcategory": "Door",
            "complaint_description": "Door hinge is broken",
            "complaint_status": "Pending",
            "reported_at": "2024-01-01T10:00:00Z",
            "sent_toEMS": true
        }
    }
    """
    permission_classes = [IsSuperintendent]

    def post(self, request):
        
        complaint_data = request.data.copy()
        complaint_data['user'] = request.user.id
        complaint_data['sent_toEMS'] = True  #mark as sent to EMS
        
        serializer = BhavanComplaintsSerializer(data=complaint_data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'message': 'Complaint created successfully',
                    'complaint_data': serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        
        return Response(
            {
                'message': 'Invalid complaint data',
                'errors': serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

#list all the complaints for supri
class ListAllComplaintAPIView(APIView):
    """
    lists all active complaints (Pending, Approved) for supri
    
    permissions:
        - User must be a Superintendent
    """
    permission_classes = [IsSuperintendent]

    def get(self, request):
        active_statuses = ['Pending', 'Approved','In_progress']
        complaints = BhavanComplaints.objects.filter(
            complaint_status__in=active_statuses
        ).order_by('-reported_at')
        
        serializer = BhavanComplaintsSerializer(complaints, many=True)
        return Response({
            'message': 'All active complaints retrieved successfully',
            'complaints': serializer.data
        })

#list al the previous compaints for supri
class ListAllPreviousComplaintAPIView(APIView):
    """
    permissions:
        - User must be a Superintendent

    Response:
    {
        "message": "All previous complaints retrieved successfully",
        "total_complaints": 2,
        "complaints": [
            {
                "id": 1,
                "user": {
                    "id": 1,
                    "username": "student1",
                    "email": "student1@example.com"
                },
                "block": "0",
                "floor": "1",
                "room_number": "101",
                "toilet": "T1",
                "request_related": "Carpenter",
                "subcategory": "Door",
                "complaint_description": "Door hinge was broken",
                "complaint_status": "Resolved",
                "reported_at": "2024-01-01T10:00:00Z",
                "resolution_details": {
                    "resolved_at": "2024-01-03T15:30:00Z",
                    "duration": "2 days, 5 hours, 30 minutes"
                }
            },
            {
                "id": 2,
                "user": {
                    "id": 2,
                    "username": "student2",
                    "email": "student2@example.com"
                },
                "block": "1",
                "floor": "2",
                "room_number": "201",
                "toilet": "T2",
                "request_related": "Plumber",
                "subcategory": "Flush Not Working",
                "complaint_description": "Bathroom flush was not working",
                "complaint_status": "Resolved",
                "reported_at": "2024-01-02T11:30:00Z",
                "resolution_details": {
                    "resolved_at": "2024-01-04T09:45:00Z",
                    "duration": "1 day, 22 hours, 15 minutes"
                }
            }
        ],
        "statistics": {
            "total_resolved": 2,
            "average_resolution_time": "2 days, 1 hour, 52 minutes",
            "complaints_by_category": {
                "Carpenter": 1,
                "Plumber": 1
            }
        }
    }
    Lists all complaints created by Supri and those with 'In Progress' status.
    """
    permission_classes = [IsSuperintendent]

    def get(self, request):
        supri = request.user  # Assuming `request.user` is Supri
        complaints = BhavanComplaints.objects.filter(
            models.Q(user=supri) | models.Q(complaint_status='In_progress')
        ).order_by('-reported_at')
        
        serializer = BhavanComplaintsSerializer(complaints, many=True)
        return Response({
            'message': 'Complaints retrieved successfully',
            'complaints': serializer.data
        })

#warden api
class ListWardenComplaintsAPIView(APIView):
    """
    lists all complaints for wardens without showing status
    
    Permissions:
        - User must be a Warden
    
    Response:
    {
        "message": "Complaints retrieved successfully",
        "total_complaints": 2,
        "complaints": [
            {
                "id": 1,
                "user": 1,
                "block": "0",
                "floor": "1",
                "room_number": "101",
                "toilet": "T1",
                "request_related": "Carpenter",
                "subcategory": "Door",
                "complaint_description": "Door hinge is broken",
                "reported_at": "2024-01-01T10:00:00Z"
            },
            {
                "id": 2,
                "user": 2,
                "block": "1",
                "floor": "2",
                "room_number": "201",
                "toilet": "T2",
                "request_related": "Plumber",
                "subcategory": "Flush Not Working",
                "complaint_description": "Bathroom flush is not working properly",
                "reported_at": "2024-01-02T11:30:00Z"
            }
        ]
    }
    """
    permission_classes = [IsWarden]

    def get(self, request):
        complaints = BhavanComplaints.objects.all().order_by('-reported_at') #in decending order by date created 
        serializer = WardenComplaintsSerializer(complaints, many=True)
        
        return Response({
            'message': 'Complaints retrieved successfully',
            'total_complaints': len(serializer.data),
            'complaints': serializer.data
        })

#estate management unit 

class EstateManagerComplaintsView(APIView):
    """
    API endpoint for Estate Manager to view and manage complaints.
    
    Permissions:
        - user must be an Estate Manager
    
    GET Response:
    {
        "message": "Complaints retrieved successfully",
        "complaints": [
            {
                "serial_number": "EMS/2024/03/0001",
                "id": 1,
                "user_details": {
                    "name": "John Doe",
                    "email": "john@example.com",
                },
                "location_details": {
                    "block": "Block 1",
                    "floor": "First Floor",
                    "room_number": "101",
                    "toilet": "Toilet 1"
                },
                "maintenance_details": {
                    "category": "Carpenter",
                    "subcategory": "Door"
                },
                "complaint_description": "Door hinge is broken",
                "formatted_date": "01-03-2024 10:30"
            },
            ...
        ]
    }
    """
    permission_classes = [IsEstateManager]

    def get(self, request):
       
        complaints = BhavanComplaints.objects.filter(
            sent_toEMS=True
        ).order_by('-reported_at')
        
        serializer = EstateManagerComplaintSerializer(complaints, many=True)
        return Response({
            'message': 'Complaints retrieved successfully',
            'complaints': serializer.data
        })

    def get_receipt(self, request, serial_number):
        """
        makeing printable receipt for a specific complaint
        
        Response:
        {
            "message": "Receipt generated successfully",
            "receipt_data": {
                "serial_number": "EMS/2024/03/0001",
                "date": "01-03-2024",
                "time": "10:30",
                "location": "Block 1, First Floor, Room 101",
                "complaint_type": "Carpenter - Door",
                "description": "Door hinge is broken",
                "student_details": {
                    "name": "John Doe",
                    "contact": "1234567890"
                }
            }
        }
        """
        try:
            complaint_id = int(serial_number.split('/')[-1])
            complaint = BhavanComplaints.objects.get(id=complaint_id)
            
            receipt_data = {
                "serial_number": serial_number,
                "date": complaint.reported_at.strftime("%d-%m-%Y"),
                "time": complaint.reported_at.strftime("%H:%M"),
                "location": f"{complaint.get_block_display()}, {complaint.get_floor_display()}, Room {complaint.room_number}",
                "complaint_type": f"{complaint.request_related} - {complaint.subcategory}",
                "description": complaint.complaint_description,
                "student_details": {
                    "name": complaint.user.get_full_name() or complaint.user.username,
                    "contact": getattr(complaint.user, 'phone_number', 'N/A')
                }
            }
            
            return Response({
                "message": "Receipt generated successfully",
                "receipt_data": receipt_data
            })
            
        except BhavanComplaints.DoesNotExist:
            return Response({
                "message": "Complaint not found",
                "error": "Invalid serial number"
            }, status=status.HTTP_404_NOT_FOUND)

class ResolveComplaintAPIView(APIView):
    """
    API endpoint to update the status of a complaint to 'Resolved'.
    Permissions:
        - Requires authentication so that anyone can use this api endpoint from supri to stdent 
    """
    permission_classes = [IsAuthenticated]

    def put(self, request, complaint_id):
        try:
           
            complaint = BhavanComplaints.objects.get(id=complaint_id)
            
            if complaint.complaint_status == 'Resolved':
                return Response({
                    'message': 'Complaint is already resolved'
                }, status=status.HTTP_400_BAD_REQUEST)
            complaint.complaint_status = 'Resolved'
            complaint.save()
   
            serializer = BhavanComplaintsSerializer(complaint)
            return Response({
                'message': 'Complaint status updated to Resolved successfully',
                'complaint': serializer.data
            }, status=status.HTTP_200_OK)
        
        except BhavanComplaints.DoesNotExist:
            return Response({
                'message': 'Complaint not found',
                'errors': {'detail': f'No complaint found with id {complaint_id}'}
            }, status=status.HTTP_404_NOT_FOUND)
