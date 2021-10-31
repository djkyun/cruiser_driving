# Generated by Django 3.1.1 on 2021-10-31 14:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_page', '0009_auto_20211030_0345'),
    ]

    operations = [
        migrations.CreateModel(
            name='LessonDetail',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('lesson_id', models.IntegerField(default=1)),
                ('lesson_detail', models.CharField(default='lesson_detail', max_length=125)),
            ],
        ),
        migrations.CreateModel(
            name='LessonDetailTitle',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('lesson_detail_id', models.IntegerField(default=1)),
                ('lesson_detail_title', models.CharField(default='lesson_detail_title', max_length=125)),
            ],
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='lesson_detail',
        ),
        migrations.AlterField(
            model_name='appointment',
            name='datetime_processed',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 31, 22, 20, 15, 438257)),
        ),
        migrations.AlterField(
            model_name='cartype',
            name='datetime_added',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 31, 22, 20, 15, 420554)),
        ),
        migrations.AlterField(
            model_name='categorytype',
            name='datetime_added',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 31, 22, 20, 15, 420554)),
        ),
        migrations.AlterField(
            model_name='enrolment',
            name='datetime_enrolled',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 31, 22, 20, 15, 420554)),
        ),
        migrations.AlterField(
            model_name='enrolment',
            name='datetime_finished',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 31, 22, 20, 15, 420554)),
        ),
        migrations.AlterField(
            model_name='enrolment',
            name='datetime_registered',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 31, 22, 20, 15, 420554)),
        ),
        migrations.AlterField(
            model_name='enrolment',
            name='datetime_start',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 31, 22, 20, 15, 420554)),
        ),
        migrations.AlterField(
            model_name='instructorspecialization',
            name='datetime_assigned',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 31, 22, 20, 15, 420554)),
        ),
        migrations.AlterField(
            model_name='rooms',
            name='datetime_added',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 31, 22, 20, 15, 420554)),
        ),
        migrations.AlterField(
            model_name='salestransaction',
            name='datetime_declared_payment',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 31, 22, 20, 15, 420554)),
        ),
        migrations.AlterField(
            model_name='salestransaction',
            name='datetime_paid',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 31, 22, 20, 15, 420554)),
        ),
        migrations.AlterField(
            model_name='schoolyear',
            name='datetime_added',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 31, 22, 20, 15, 420554)),
        ),
        migrations.AlterField(
            model_name='systemsettings',
            name='datetime_last_update',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 31, 22, 20, 15, 420554), max_length=225),
        ),
        migrations.AlterField(
            model_name='timescheduleappointment',
            name='class_datetime',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 31, 22, 20, 15, 436180)),
        ),
        migrations.AlterField(
            model_name='timescheduleappointment',
            name='datetime_assigned',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 31, 22, 20, 15, 436180)),
        ),
    ]
