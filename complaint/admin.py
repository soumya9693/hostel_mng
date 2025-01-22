from django.contrib import admin
from .models import BhavanComplaints

@admin.register(BhavanComplaints) #based on latest documentation basically its better implementation 
class BhavanComplaintsAdmin(admin.ModelAdmin):
    list_display = (
        'user', 
        'block', 
        'floor', 
        'room_number', 
        'toilet', 
        'request_related', 
        'subcategory', 
        'complaint_status', 
        'reported_at',
        'sent_toEMS'
    )
    
    list_filter = (
        'block', 
        'floor', 
        'request_related', 
        'complaint_status', 
        'reported_at'
    )
    
    search_fields = (
        'user__username', 
        'room_number', 
        'complaint_description', 
        'block', 
        'request_related', 
        'subcategory'
    )
    
    ordering = ('-reported_at',)
    readonly_fields = ('reported_at',)
    
   
    fieldsets = (
        ('Complaint Details', {
            'fields': (
                'user', 
                'block', 
                'floor', 
                'room_number', 
                'toilet'
            )
        }),
        ('Request Information', {
            'fields': (
                'request_related', 
                'subcategory', 
                'complaint_description'
            )
        }),
        ('Status', {
            'fields': (
                'complaint_status',
                'sent_toEMS',
                'reported_at'
            )
        }),
    )