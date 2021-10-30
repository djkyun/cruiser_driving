from django.db import models
import datetime

# Create your models here.
        
class LoginHistory(models.Model):

    datetime_login                     = models.CharField(max_length=50, default = "--")
    datetime_logout                    = models.CharField(max_length=50, default = "--")
    user_id                            = models.CharField(max_length=20, default = "--")
     
    def __str__(self):
     
       return self.user_id
  
        
class CarType(models.Model):
    
    id                                  = models.AutoField(primary_key = True)
    car_type_name                       = models.CharField(max_length = 125, default = 'Manual')
    added_by                            = models.CharField(max_length = 125)
    datetime_added                      = models.DateTimeField(default = datetime.datetime.now())
    
    def __str__(self):
    
        return self.id
        
class CategoryType(models.Model):

    id                                  = models.AutoField(primary_key = True)
    category_type_name                  = models.CharField(max_length = 125, default = 'Manual')
    added_by                            = models.CharField(max_length = 125)
    datetime_added                      = models.DateTimeField(default = datetime.datetime.now())
    
    def __str__(self):
    
        return self.id
     
class Category(models.Model):

    id                                  = models.AutoField(primary_key = True)
    category_name                       = models.CharField(max_length = 125, default = 'Regular')
    category_type_id                    = models.IntegerField(default = 1)
    
    def __str__(self):
        return self.id    
      
class Course(models.Model):

    id                                  = models.AutoField(primary_key = True)
    course_code                         = models.CharField(max_length = 15, default = 'C15S')
    course_name                         = models.CharField(max_length = 225, default = '15 Hours')
    course_description                  = models.CharField(max_length = 225, default = 'Basic Driving')    
    hours_duration                      = models.CharField(max_length = 5, default = '5')
    added_by                            = models.CharField(max_length = 125, default = 'ADMIN1')
    datetime_added                      = models.CharField(max_length = 125, default = '9-10-2021 10:06:45')
    category_type_id                    = models.IntegerField(default = 1)
    category_id                         = models.IntegerField(default = 1)
    car_type_id                         = models.IntegerField(default = 1)
    tuition_fee                         = models.CharField(max_length = 10, default = '4999')
    
    def __str__(self):
        return self.id
        
        
class SystemSettings(models.Model):

    id                                  = models.AutoField(primary_key = True)
    system_label                        = models.CharField(max_length = 225, default = 'system_label')
    system_name                         = models.CharField(max_length = 225, default = 'system_name')
    system_value                        = models.CharField(max_length = 1025, default = 'system_value')
    system_other_value                  = models.CharField(max_length = 1025, default = 'system_other_value')    
    datetime_last_update                = models.DateTimeField(max_length = 225, default = datetime.datetime.now())
    updated_by                          = models.CharField(max_length = 125, default = 'updated_by')
    status                              = models.CharField(max_length = 1, default = '1')
    
    def __str__(self):
        return self.id
        
class Enrolment(models.Model):

    id                                  = models.AutoField(primary_key = True)
    user_id                             = models.CharField(max_length = 125, default = '0')
    license_type                        = models.CharField(max_length = 2, default = '1')
    enrolled_course                     = models.CharField(max_length = 10, default = '0')
    payment_method                      = models.CharField(max_length = 2, default = '0')
    payment_term                        = models.CharField(max_length = 2, default = '0')   
    amount                              = models.CharField(max_length = 7, default = '15999')
    datetime_registered                 = models.DateTimeField(default = datetime.datetime.now())
    datetime_enrolled                   = models.DateTimeField(default = datetime.datetime.now())
    datetime_start                      = models.DateTimeField(default = datetime.datetime.now())
    datetime_finished                   = models.DateTimeField(default = datetime.datetime.now())
    status                              = models.CharField(max_length = 1, default = '0')   
    processed_by                        = models.CharField(max_length = 125, default = '0')
    finished_processed_by               = models.CharField(max_length = 125, default = '0')
    
    # license_type
    # none = 0, student permit = 1, non professional = 2, professional = 3
    
    def __str__(self):
        return self.id
        
class SalesTransaction(models.Model):

    id                                  = models.AutoField(primary_key = True)
    enrolment_id                        = models.IntegerField(default = 1)
    amount_paid                         = models.CharField(max_length = 10, default = '--')
    amount_balance                      = models.CharField(max_length = 10, default = '0')
    user_id                             = models.CharField(max_length = 125, default = '1')
    user_contact_number                 = models.CharField(max_length = 15, default = '1')
    payment_reference_no                = models.CharField(max_length = 125, default = '1')
    payment_contact_number              = models.CharField(max_length = 15, default = '1')
    transaction_type                    = models.IntegerField(default = 2)
    payment_method                      = models.CharField(max_length = 2, default = '1')
    payment_term                        = models.CharField(max_length = 1, default = '1')
    for_payment_term                    = models.IntegerField(default = 1)
    datetime_paid                       = models.DateTimeField(default = datetime.datetime.now())
    datetime_declared_payment           = models.DateTimeField(default = datetime.datetime.now())
    processed_by                        = models.CharField(max_length = 125, default = '1')
    status                              = models.IntegerField(default = 0)
    
    def __str__(self):
        return self.id    
        
    def reference_number(self):
        return datetime.datetime.now().strftime("%Y-%m-%D-") + str(self.id)
        
class LessonRecord(models.Model):

    id                              = models.AutoField(primary_key = True)
    attendance_id                   = models.IntegerField(default = 1)
    curriculum_id                   = models.IntegerField(default = 1)
    
    def __str__(self):
        return self.id
        
class ScheduleType(models.Model):

    id                              = models.AutoField(primary_key = True)
    schedules                       = models.CharField(max_length = 30, default = 'MON-TUE-WED-THUR-FRI-SAT-SUN')
    hours_per_day                   = models.IntegerField(default = 3)
    status                          = models.IntegerField(default = 1)
    added_by                        = models.CharField(max_length = 125, default = '1')
    
    def __str__(self):
        return self.id
           

class Attendance(models.Model):

   id                               = models.AutoField(primary_key = True)
   time_schedule_appointment_id     = models.CharField(max_length = 125, default = 1)
   enrolment_id                     = models.IntegerField(default = 1)
   status                           = models.IntegerField(default = 1) 
   hours_rendered                   = models.IntegerField()
   
   def __str__(self):
        return self.id
        
        
class InstructorSpecialization(models.Model):

    id                               = models.AutoField(primary_key = True)
    instructor_id                    = models.CharField(max_length = 125, default = '1')
    course_id                        = models.IntegerField(default = 1)
    assigned_by                      = models.CharField(max_length = 125)
    datetime_assigned                = models.DateTimeField(default = datetime.datetime.now())
     
    def __str__(self):
        return self.id
        
class SchoolYear(models.Model):

    id                               = models.AutoField(primary_key = True)
    schoolyear                       = models.CharField(max_length = 15)
    status                           = models.CharField(max_length = 1, default = 1)
    added_by                         = models.CharField(max_length = 125)
    last_updated_by                  = models.CharField(max_length = 125)
    datetime_added                   = models.DateTimeField(default = datetime.datetime.now())
    
    def __str__(self):
        return self.id
    
  
class Rooms(models.Model):

    id                               = models.AutoField(primary_key = True)
    room_name                        = models.CharField(max_length = 125, default = 'Ordinary Room')
    room_no                          = models.CharField(max_length = 10, default = 'ROOM 101')
    building                         = models.CharField(max_length = 125, default = 'cruiser building')
    floor                            = models.CharField(max_length = 15, default = '1st floor')
    status                           = models.CharField(max_length = 1, default = '1')
    updated_by                       = models.CharField(max_length = 125, default = '1')
    added_by                         = models.CharField(max_length = 125, default = '1')
    datetime_added                   = models.DateTimeField(default = datetime.datetime.now())
     
    def __str__(self):
        return self.id
 

        
class TimeScheduleAppointment(models.Model):

    id                              = models.AutoField(primary_key = True)
    instructor_id                   = models.CharField(max_length = 125, default = '1')
    course_id                       = models.IntegerField()
    room_id                         = models.IntegerField(default = 1)
    scheduled_day                   = models.CharField(max_length = 3, default = 'MON')
    class_datetime                  = models.DateTimeField(default = datetime.datetime.now())  
    time_start                      = models.TimeField()
    time_end                        = models.TimeField()
    assigned_by                     = models.CharField(max_length = 125)
    datetime_assigned               = models.DateTimeField(default = datetime.datetime.now())
    appointment_id                  = models.IntegerField()
    status                          = models.CharField(max_length = 1, default = '1')
    
    def __str__(self):
        return self.id
        
class Appointment(models.Model):

    id                              = models.AutoField(primary_key = True)
    batch_appointment_code          = models.CharField(max_length = 15, default = 'A11')
    batch_appointment_name          = models.CharField(max_length = 125, default = 'Class Batch')     
    schedule_type                   = models.IntegerField(default = 5)
    sy_id                           = models.IntegerField(default = 1)
    datetime_processed              = models.DateTimeField(default = datetime.datetime.now())
    processed_by                    = models.CharField(max_length = 125, default = '1')
    status                          = models.CharField(max_length = 1, default = '1')
    
    def __str__(self):
        return self.id
        
class PaymentMethodList(models.Model):
    
    id                              = models.AutoField(primary_key = True)
    payment_method                  = models.CharField(max_length = 125, default = 'CASH')
    payment_method_image            = models.CharField(max_length = 225, default = 'image.jpg')
    status                          = models.CharField(max_length = 1, default = '1')
    
    def __str__(self):
        return self.id
        
class Lesson(models.Model):
    
    id                              = models.AutoField(primary_key = True)
    course_id                       = models.CharField(max_length = 10, default = '1')
    lesson_number                   = models.IntegerField(default = 1)   
    
    def __str__(self):
        return self.id
        
class LessonDetailTitle(models.Model):

    id                              = models.AutoField(primary_key = True)
    lesson_detail_id                = models.IntegerField(default = 1)
    lesson_detail_title             = models.CharField(max_length = 125, default = 'lesson_detail_title')
    
    def __str__(self):
        return self.id
        
class LessonDetail(models.Model):

    id                              = models.AutoField(primary_key = True)
    lesson_id                       = models.IntegerField(default = 1)
    lesson_detail                   = models.CharField(max_length = 125, default = 'lesson_detail')
    
    def __str__(self):
        return self.id
        
class Curriculum(models.Model):
    
    id                              = models.AutoField(primary_key = True)
    course_id                       = models.CharField(max_length = 10, default = '1')
    lesson_number                   = models.IntegerField(default = 1)
    lesson_description              = models.CharField(max_length = 125, default = 'orientation')
    hours_duration                  = models.IntegerField(default = 1)
    status                          = models.CharField(max_length = 1, default = '1')    
    
    def __str__(self):
        return self.id
        
class SkillsAssessments(models.Model):

    id                              = models.AutoField(primary_key = True)
    course_id                       = models.CharField(max_length = 10, default = '1')
    lesson_number                   = models.IntegerField(default = 1)
    assessment_value                = models.CharField(max_length = 1)
    remarks                         = models.CharField(max_length = 225)
    instructor_id                   = models.CharField(max_length = 125, default = 'i1')
    user_id                         = models.CharField(max_length = 125, default = 'u1')
    
    def __str__(self):
        return self.id