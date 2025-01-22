from django.db import models
from django.conf import settings 


BLOCKS_CHOICES = [
    ('0', 'Block 0'),
    ('1', 'Block 1'),
    ('2', 'Block 2'),
    ('3', 'Block 3'),
    ('4', 'Block 4'),
    ('5', 'Block 5'),
    ('6', 'Block 6'),
    ('7', 'Block 7'),
    ('8', 'Block 8'),
    ('9', 'Block 9'),
    ('Qtr 75', 'Quarter 75'),
    ('Qtr 76', 'Quarter 76'),
    ('Qtr 77', 'Quarter 77'),
    ('Qtr 78', 'Quarter 78'),
    ('Qtr 79', 'Quarter 79'),
    ('Qtr 80', 'Quarter 80'),
    ('Common Area', 'Common Area'),
    ('Visitors Room', 'Visitors Room'),
    ('Mess', 'Mess'),
]

FLOOR_CHOICES = [
    ('0', 'Ground Floor'),
    ('1', 'First Floor'),
    ('2', 'Second Floor'),
    ('3', 'Third Floor'),
]

TOILET_CHOICES = [
    ('T1', 'Toilet 1'),
    ('T2', 'Toilet 2'),
    ('T3', 'Toilet 3'),
    ('T4', 'Toilet 4'),
    ('T5', 'Toilet 5'),
    ('T6', 'Toilet 6'),
    ('T7', 'Toilet 7'),
    ('T8', 'Toilet 8'),
    ('T9', 'Toilet 9'),
    ('T10', 'Toilet 10'),
    ('T11', 'Toilet 11'),
    ('T12', 'Toilet 12'),
]

REQUEST_RELATED_CHOICES = [
    ('Carpenter', 'Carpenter'),
    ('Sweeper', 'Sweeper'),
    ('Gardener', 'Gardener'),
    ('Plumber', 'Plumber'),
    ('RO Person', 'RO Person'),
    ('Electrician', 'Electrician'),
    ('Mason', 'Mason'),
    ('Painter', 'Painter'),
    ('Worker', 'Worker'),
]

CARPENTER_SUBCATEGORY_CHOICES = [
    ('Door', 'Door'),
    ('Clothes Rope', 'Clothes Rope'),
    ('Fixing Curtain Rod', 'Fixing Curtain Rod'),
    ('Hanger Unavailable', 'Hanger Unavailable'),
    ('Almirah', 'Almirah'),
    ('Room Door Locked', 'Room Door Locked'),
    ('Others', 'Others'),
]

SWEEPER_SUBCATEGORY_CHOICES = [
    ('Sewer Line', 'Sewer Line'),
    ('Balcony Drain Hole Blocked', 'Balcony Drain Hole Blocked'),
    ('Sink Drain Hole Blocked', 'Sink Drain Hole Blocked'),
    ('Flush Blocked', 'Flush Blocked'),
    ('Bathroom Drain Hole Blocked', 'Bathroom Drain Hole Blocked'),
    ('Garbage Removal', 'Garbage Removal'),
    ('Others', 'Others'),
]

GARDENER_SUBCATEGORY_CHOICES = [
    ('Tree Trimming', 'Tree Trimming'),
    ('Others', 'Others'),
]

PLUMBER_SUBCATEGORY_CHOICES = [
    ('Flush Not Working', 'Flush Not Working'),
    ('Sink Tap Not Working', 'Sink Tap Not Working'),
    ('Flush Dirty Water', 'Flush Dirty Water'),
    ('Sink Dirty Water', 'Sink Dirty Water'),
    ('Jet Spray Not Working', 'Jet Spray Not Working'),
    ('Jet Spray Dirty Water', 'Jet Spray Dirty Water'),
    ('Indian Toilet Tap Not Working', 'Indian Toilet Tap Not Working'),
    ('Indian Toilet Tap Dirty Water', 'Indian Toilet Tap Dirty Water'),
    ('Bathroom Tap Not Working', 'Bathroom Tap Not Working'),
    ('Bathroom Tap Dirty Water', 'Bathroom Tap Dirty Water'),
    ('Others', 'Others'),
]

RO_SUBCATEGORY_CHOICES = [
    ('Dirty Water', 'Dirty Water'),
    ('Drain Hole Blocked', 'Drain Hole Blocked'),
    ('RO Cleaning', 'RO Cleaning'),
    ('Others', 'Others'),
]

ELECTRICIAN_SUBCATEGORY_CHOICES = [
    ('Room Switch Repair/Replacement', 'Room Switch Repair/Replacement'),
    ('Room Tube Light Repair/Replacement', 'Room Tube Light Repair/Replacement'),
    ('Room Fan Repair/Replacement', 'Room Fan Repair/Replacement'),
    ('Room Exhaust Fan Repair/Replacement', 'Room Exhaust Fan Repair/Replacement'),
    ('Corridor Light Repair/Replacement', 'Corridor Light Repair/Replacement'),
    ('Balcony Light Repair/Replacement', 'Balcony Light Repair/Replacement'),
    ('Bathroom Light Repair/Replacement', 'Bathroom Light Repair/Replacement'),
    ('Corridor Switch Repair/Replacement', 'Corridor Switch Repair/Replacement'),
    ('Bathroom Exhaust Fan Repair/Not Working', 'Bathroom Exhaust Fan Repair/Not Working'),
    ('Geyser Repair/Replacement', 'Geyser Repair/Replacement'),
    ('Common Room AC Repair/Replacement', 'Common Room AC Repair/Replacement'),
    ('Common Room TV Repair/Replacement', 'Common Room TV Repair/Replacement'),
    ('Common Room Fan Repair/Replacement', 'Common Room Fan Repair/Replacement'),
    ('Common Room Light Repair/Replacement', 'Common Room Light Repair/Replacement'),
    ('Others', 'Others'),
]

MASON_SUBCATEGORY_CHOICES = [
    ('Room Floor Repair', 'Room Floor Repair'),
    ('Bathroom Wall Repair', 'Bathroom Wall Repair'),
    ('Bathroom Floor Repair', 'Bathroom Floor Repair'),
    ('Room Wall Repair', 'Room Wall Repair'),
    ('Others', 'Others'),
]

PAINTER_SUBCATEGORY_CHOICES = [
    ('Whitewash', 'Whitewash'),
    ('Paint on the Door Window', 'Paint on the Door Window'),
    ('Paint on Window Frames', 'Paint on Window Frames'),
    ('Others', 'Others'),
]

WORKER_SUBCATEGORY_CHOICES = [
    ('Shift Heavy Goods', 'Shift Heavy Goods'),
    ('Others', 'Others'), #not in pdf still added 

]

COMPLAINT_STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('Approved','Approved'),
    ('In_progress','In_progress'),
    ('Resolved', 'Resolved')
]

#have put null and blank true frontend should implement necessary checks 

class BhavanComplaints(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  
        on_delete=models.CASCADE,  
        related_name='complaints',  # reverse relation name
        verbose_name='Complaint Owner'
    )

    block = models.CharField(
        max_length=20, 
        choices=BLOCKS_CHOICES, 
        verbose_name="Block/Quarter",
        null = True,
        blank = True
    )

    floor = models.CharField(
        max_length=1, 
        choices=FLOOR_CHOICES, 
        verbose_name="Floor",
        null = True,
        blank = True
    )
    room_number = models.CharField(
        max_length=10, 
        verbose_name="Room Number",
        null = True,
        blank = True
    )

    toilet = models.CharField(
        max_length=3, 
        choices=TOILET_CHOICES, 
        verbose_name="Toilet",
        null = True,
        blank = True
    )

    request_related = models.CharField(
        max_length=20, 
        choices=REQUEST_RELATED_CHOICES, 
        verbose_name="Request Related To",
        null = True,
        blank = True
    )
    
  
    subcategory = models.CharField(
        max_length=50, 
        verbose_name="Subcategory",
        null = True,
        blank = True
    )
    
    complaint_description = models.TextField(
        blank=True, 
        null=True, 
        verbose_name="Complaint Description"
    )

    complaint_status = models.CharField(
        max_length=20, 
        choices=COMPLAINT_STATUS_CHOICES, 
        default='Pending', 
        verbose_name="Complaint Status"
    )


    reported_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="Reported Date and Time"
    )

    sent_toEMS = models.BooleanField(default=False)
    def clean(self):
    
        from django.core.exceptions import ValidationError
        
        subcategory_map = {
            'Carpenter': CARPENTER_SUBCATEGORY_CHOICES,
            'Sweeper': SWEEPER_SUBCATEGORY_CHOICES,
            'Gardener': GARDENER_SUBCATEGORY_CHOICES,
            'Plumber': PLUMBER_SUBCATEGORY_CHOICES,
            'RO Person': RO_SUBCATEGORY_CHOICES,
            'Electrician': ELECTRICIAN_SUBCATEGORY_CHOICES,
            'Mason': MASON_SUBCATEGORY_CHOICES,
            'Painter': PAINTER_SUBCATEGORY_CHOICES,
            'Worker': WORKER_SUBCATEGORY_CHOICES
        }
        
        valid_subcategories = [choice[0] for choice in subcategory_map.get(self.request_related, [])]
        
        if self.subcategory not in valid_subcategories:
            raise ValidationError({
                'subcategory': f'Invalid subcategory for {self.request_related}'
            })

    def __str__(self):
        return (
            f"{self.get_block_display()} - "
            f"Floor {self.get_floor_display()} - "
            f"Room {self.room_number} - "
            f"{self.get_toilet_display()} - "
            f"{self.request_related} - "
            f"{self.subcategory} - "
            f"Status: {self.get_complaint_status_display()}"
        )

    class Meta:
        verbose_name = "Bhavan Complaint"
        verbose_name_plural = "Bhavan Complaints"
        ordering = ['-reported_at']