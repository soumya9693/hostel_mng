# Generated by Django 5.1.2 on 2024-11-24 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('complaint', '0004_bhavancomplaints_sent_toems_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bhavancomplaints',
            name='complaint_status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('In_progress', 'In_progress'), ('Resolved', 'Resolved')], default='Pending', max_length=20, verbose_name='Complaint Status'),
        ),
    ]
