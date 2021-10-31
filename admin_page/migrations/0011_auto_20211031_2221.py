# Generated by Django 3.1.1 on 2021-10-31 14:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_page', '0010_auto_20211031_2220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='datetime_processed',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 31, 22, 21, 48, 948408)),
        ),
        migrations.AlterField(
            model_name='cartype',
            name='datetime_added',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 31, 22, 21, 48, 932786)),
        ),
        migrations.AlterField(
            model_name='categorytype',
            name='datetime_added',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 31, 22, 21, 48, 932786)),
        ),
        migrations.AlterField(
            model_name='enrolment',
            name='datetime_enrolled',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 31, 22, 21, 48, 948408)),
        ),
        migrations.AlterField(
            model_name='enrolment',
            name='datetime_finished',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 31, 22, 21, 48, 948408)),
        ),
        migrations.AlterField(
            model_name='enrolment',
            name='datetime_registered',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 31, 22, 21, 48, 948408)),
        ),
        migrations.AlterField(
            model_name='enrolment',
            name='datetime_start',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 31, 22, 21, 48, 948408)),
        ),
        migrations.AlterField(
            model_name='instructorspecialization',
            name='datetime_assigned',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 31, 22, 21, 48, 948408)),
        ),
        migrations.AlterField(
            model_name='rooms',
            name='datetime_added',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 31, 22, 21, 48, 948408)),
        ),
        migrations.AlterField(
            model_name='salestransaction',
            name='datetime_declared_payment',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 31, 22, 21, 48, 948408)),
        ),
        migrations.AlterField(
            model_name='salestransaction',
            name='datetime_paid',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 31, 22, 21, 48, 948408)),
        ),
        migrations.AlterField(
            model_name='schoolyear',
            name='datetime_added',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 31, 22, 21, 48, 948408)),
        ),
        migrations.AlterField(
            model_name='systemsettings',
            name='datetime_last_update',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 31, 22, 21, 48, 932786), max_length=225),
        ),
        migrations.AlterField(
            model_name='timescheduleappointment',
            name='class_datetime',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 31, 22, 21, 48, 948408)),
        ),
        migrations.AlterField(
            model_name='timescheduleappointment',
            name='datetime_assigned',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 31, 22, 21, 48, 948408)),
        ),
    ]
