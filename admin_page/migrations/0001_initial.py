# Generated by Django 3.1.1 on 2021-10-20 19:02

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('batch_appointment_code', models.CharField(default='A11', max_length=15)),
                ('batch_appointment_name', models.CharField(default='Class Batch', max_length=125)),
                ('schedule_type', models.IntegerField(default=5)),
                ('sy_id', models.IntegerField(default=1)),
                ('datetime_processed', models.DateTimeField(default=datetime.datetime(2021, 10, 21, 3, 2, 24, 986667))),
                ('processed_by', models.CharField(default='1', max_length=125)),
                ('status', models.CharField(default='1', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('time_schedule_appointment_id', models.CharField(default=1, max_length=125)),
                ('enrolment_id', models.IntegerField(default=1)),
                ('status', models.IntegerField(default=1)),
                ('hours_rendered', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='CarType',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('car_type_name', models.CharField(default='Manual', max_length=125)),
                ('added_by', models.CharField(max_length=125)),
                ('datetime_added', models.DateTimeField(default=datetime.datetime(2021, 10, 21, 3, 2, 24, 986667))),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('category_name', models.CharField(default='Regular', max_length=125)),
                ('category_type_id', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='CategoryType',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('category_type_name', models.CharField(default='Manual', max_length=125)),
                ('added_by', models.CharField(max_length=125)),
                ('datetime_added', models.DateTimeField(default=datetime.datetime(2021, 10, 21, 3, 2, 24, 986667))),
            ],
        ),
        migrations.CreateModel(
            name='Curriculum',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('course_id', models.CharField(default='1', max_length=10)),
                ('lesson_number', models.IntegerField(default=1)),
                ('lesson_description', models.CharField(default='orientation', max_length=125)),
                ('hours_duration', models.IntegerField(default=1)),
                ('status', models.CharField(default='1', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Enrolment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.CharField(default='0', max_length=125)),
                ('enrolled_course', models.CharField(default='0', max_length=10)),
                ('payment_method', models.CharField(default='0', max_length=2)),
                ('payment_term', models.CharField(default='0', max_length=2)),
                ('amount', models.CharField(default='15999', max_length=7)),
                ('datetime_registered', models.DateTimeField(default=datetime.datetime(2021, 10, 21, 3, 2, 24, 986667))),
                ('datetime_enrolled', models.DateTimeField(default=datetime.datetime(2021, 10, 21, 3, 2, 24, 986667))),
                ('datetime_start', models.DateTimeField(default=datetime.datetime(2021, 10, 21, 3, 2, 24, 986667))),
                ('datetime_finished', models.DateTimeField(default=datetime.datetime(2021, 10, 21, 3, 2, 24, 986667))),
                ('status', models.CharField(default='0', max_length=1)),
                ('processed_by', models.CharField(default='0', max_length=125)),
                ('finished_processed_by', models.CharField(default='0', max_length=125)),
            ],
        ),
        migrations.CreateModel(
            name='InstructorSpecialization',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('instructor_id', models.CharField(default='1', max_length=125)),
                ('course_id', models.IntegerField(default=1)),
                ('assigned_by', models.CharField(max_length=125)),
                ('datetime_assigned', models.DateTimeField(default=datetime.datetime(2021, 10, 21, 3, 2, 24, 986667))),
            ],
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('course_id', models.CharField(default='1', max_length=10)),
                ('lesson_number', models.IntegerField(default=1)),
                ('lesson_detail', models.CharField(default='orientation', max_length=125)),
            ],
        ),
        migrations.CreateModel(
            name='LessonRecord',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('attendance_id', models.IntegerField(default=1)),
                ('curriculum_id', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='LoginHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_login', models.CharField(default='--', max_length=50)),
                ('datetime_logout', models.CharField(default='--', max_length=50)),
                ('user_id', models.CharField(default='--', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='PaymentMethodList',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('payment_method', models.CharField(default='CASH', max_length=125)),
                ('payment_method_image', models.CharField(default='image.jpg', max_length=225)),
                ('status', models.CharField(default='1', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Rooms',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('room_name', models.CharField(default='Ordinary Room', max_length=125)),
                ('room_no', models.CharField(default='ROOM 101', max_length=10)),
                ('building', models.CharField(default='cruiser building', max_length=125)),
                ('floor', models.CharField(default='1st floor', max_length=15)),
                ('status', models.CharField(default='1', max_length=1)),
                ('updated_by', models.CharField(default='1', max_length=125)),
                ('added_by', models.CharField(default='1', max_length=125)),
                ('datetime_added', models.DateTimeField(default=datetime.datetime(2021, 10, 21, 3, 2, 24, 986667))),
            ],
        ),
        migrations.CreateModel(
            name='SalesTransaction',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('enrolment_id', models.IntegerField(default=1)),
                ('amount_paid', models.CharField(default='--', max_length=10)),
                ('amount_balance', models.CharField(default='0', max_length=10)),
                ('user_id', models.CharField(default='1', max_length=125)),
                ('user_contact_number', models.CharField(default='1', max_length=15)),
                ('payment_reference_no', models.CharField(default='1', max_length=125)),
                ('payment_contact_number', models.CharField(default='1', max_length=15)),
                ('transaction_type', models.IntegerField(default=2)),
                ('payment_method', models.CharField(default='1', max_length=2)),
                ('payment_term', models.CharField(default='1', max_length=1)),
                ('for_payment_term', models.IntegerField(default=1)),
                ('datetime_paid', models.DateTimeField(default=datetime.datetime(2021, 10, 21, 3, 2, 24, 986667))),
                ('datetime_declared_payment', models.DateTimeField(default=datetime.datetime(2021, 10, 21, 3, 2, 24, 986667))),
                ('processed_by', models.CharField(default='1', max_length=125)),
                ('status', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='ScheduleType',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('schedules', models.CharField(default='MON-TUE-WED-THUR-FRI-SAT-SUN', max_length=30)),
                ('hours_per_day', models.IntegerField(default=3)),
                ('status', models.IntegerField(default=1)),
                ('added_by', models.CharField(default='1', max_length=125)),
            ],
        ),
        migrations.CreateModel(
            name='SchoolYear',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('schoolyear', models.CharField(max_length=15)),
                ('status', models.CharField(default=1, max_length=1)),
                ('added_by', models.CharField(max_length=125)),
                ('last_updated_by', models.CharField(max_length=125)),
                ('datetime_added', models.DateTimeField(default=datetime.datetime(2021, 10, 21, 3, 2, 24, 986667))),
            ],
        ),
        migrations.CreateModel(
            name='SkillsAssessments',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('course_id', models.CharField(default='1', max_length=10)),
                ('lesson_number', models.IntegerField(default=1)),
                ('assessment_value', models.CharField(max_length=1)),
                ('remarks', models.CharField(max_length=225)),
                ('instructor_id', models.CharField(default='i1', max_length=125)),
                ('user_id', models.CharField(default='u1', max_length=125)),
            ],
        ),
        migrations.CreateModel(
            name='SystemSettings',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('system_label', models.CharField(default='system_label', max_length=225)),
                ('system_name', models.CharField(default='system_name', max_length=225)),
                ('system_value', models.CharField(default='system_value', max_length=1025)),
                ('system_other_value', models.CharField(default='system_other_value', max_length=1025)),
                ('datetime_last_update', models.DateTimeField(default=datetime.datetime(2021, 10, 21, 3, 2, 24, 986667), max_length=225)),
                ('updated_by', models.CharField(default='updated_by', max_length=125)),
                ('status', models.CharField(default='1', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='TimeScheduleAppointment',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('instructor_id', models.CharField(default='1', max_length=125)),
                ('course_id', models.IntegerField()),
                ('room_id', models.IntegerField(default=1)),
                ('scheduled_day', models.CharField(default='MON', max_length=3)),
                ('class_datetime', models.DateTimeField(default=datetime.datetime(2021, 10, 21, 3, 2, 24, 986667))),
                ('time_start', models.TimeField()),
                ('time_end', models.TimeField()),
                ('assigned_by', models.CharField(max_length=125)),
                ('datetime_assigned', models.DateTimeField(default=datetime.datetime(2021, 10, 21, 3, 2, 24, 986667))),
                ('appointment_id', models.IntegerField()),
                ('status', models.CharField(default='1', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('course_code', models.CharField(default='C15S', max_length=15)),
                ('course_name', models.CharField(default='15 Hours', max_length=225)),
                ('course_description', models.CharField(default='Basic Driving', max_length=225)),
                ('hours_duration', models.CharField(default='5', max_length=5)),
                ('added_by', models.CharField(default='ADMIN1', max_length=125)),
                ('datetime_added', models.CharField(default='9-10-2021 10:06:45', max_length=125)),
                ('category_id', models.IntegerField(default=1)),
                ('car_type_id', models.IntegerField(default=1)),
                ('tuition_fee', models.CharField(default='4999', max_length=10)),
                ('category_type_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_page.categorytype')),
            ],
        ),
    ]
