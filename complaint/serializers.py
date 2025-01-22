from rest_framework import serializers
from .models import BhavanComplaints

class BhavanComplaintsSerializer(serializers.ModelSerializer):
    block = serializers.CharField(required=False, allow_blank=True)
    floor = serializers.IntegerField(required=False)
    room_number = serializers.CharField(required=False, allow_blank=True)
    toilet = serializers.CharField(required=False, allow_blank=True)
    request_related = serializers.CharField(required=False, allow_blank=True)
    subcategory = serializers.CharField(required=False, allow_blank=True)
    complaint_description = serializers.CharField(required=False, allow_blank=True)
    complaint_status = serializers.CharField(required=False, allow_blank=True)
    # reported_at = serializers.DateTimeField(required=False)
    class Meta:
        model = BhavanComplaints
        fields = [
            'id', 'user', 'block', 'floor', 'room_number', 
            'toilet', 'request_related', 'subcategory', 
            'complaint_description', 'complaint_status', 'reported_at','sent_toEMS'
        ]
        read_only_fields = ['id', 'complaint_status', 'reported_at']


class WardenComplaintsSerializer(serializers.ModelSerializer):
    """
    serializer for warden - excludes complaint status
    """
    class Meta:
        model = BhavanComplaints
        fields = [
            'id', 'user', 'block', 'floor', 'room_number', 
            'toilet', 'request_related', 'subcategory', 
            'complaint_description', 'reported_at'
        ]
        read_only_fields = ['id', 'reported_at']

class EstateManagerComplaintSerializer(serializers.ModelSerializer):
    serial_number = serializers.SerializerMethodField()
    user_details = serializers.SerializerMethodField()
    location_details = serializers.SerializerMethodField()
    maintenance_details = serializers.SerializerMethodField()
    formatted_date = serializers.SerializerMethodField()

    class Meta:
        model = BhavanComplaints
        fields = [
            'serial_number',
            'id',
            'user_details',
            'location_details',
            'maintenance_details',
            'complaint_description',
            'formatted_date'
        ]

    def get_serial_number(self, obj):


                   date = obj.reported_at
                   return f"EMS/{date.year}/{date.month:02d}/{obj.id:04d}"



    def get_user_details(self, obj):
        return {
            'name': obj.user.get_full_name() or obj.user.username, #for student and supri 
            'email': obj.user.email,
        }

    def get_location_details(self, obj):
        return {
            'block': obj.get_block_display(),
            'floor': obj.get_floor_display(),
            'room_number': obj.room_number,
            'toilet': obj.get_toilet_display() if obj.toilet else 'N/A'
        }

    def get_maintenance_details(self, obj):
        return {
            'category': obj.request_related,
            'subcategory': obj.subcategory
        }

    def get_formatted_date(self, obj):
        """Return formatted date string"""

        return obj.reported_at.strftime("%d-%m-%Y %H:%M")

