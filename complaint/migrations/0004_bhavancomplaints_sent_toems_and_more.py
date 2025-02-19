# Generated by Django 5.1.2 on 2024-11-02 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('complaint', '0003_alter_bhavancomplaints_block_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bhavancomplaints',
            name='sent_toEMS',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='bhavancomplaints',
            name='complaint_status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Resolved', 'Resolved')], default='Pending', max_length=20, verbose_name='Complaint Status'),
        ),
    ]
