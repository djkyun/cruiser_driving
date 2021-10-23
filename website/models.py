from django.db import models
from django.urls import reverse
import datetime, math

# Create your models here.
    
class LoginForm(models.Model):

    id = models.CharField(max_length = 50, default = '1', primary_key = True)
    username = models.CharField(max_length = 50, default = 'username')
    password = models.CharField(max_length = 50, default = 'password')
    
    def __str__(self):
        return self.id
        
class UserRecords(models.Model):

    id = models.AutoField(primary_key = True)
    authentication_user_id = models.CharField(max_length = 125, default = '1')
    firstname = models.CharField(max_length = 125, default = 'Jessica')
    lastname = models.CharField(max_length = 125, default = 'Saludes')
    middlename = models.CharField(max_length = 125, default = 'Manahan')
    name_extension = models.CharField(max_length = 5, default = ' ')
    birthdate = models.CharField(max_length = 125, default = ' ')
    complete_address = models.CharField(max_length = 125, default = ' ')
    contact_number = models.CharField(max_length = 15, default = '09101111111')
    email_address = models.CharField(max_length = 225, default = 'user@user.com')
    gender = models.CharField(max_length = 1, default = 'n')
    civil_status = models.CharField(max_length = 1, default = '1', null = True, blank = True)
    datetime_registered = models.DateTimeField(default = datetime.datetime.now())
    role_id = models.IntegerField(default = 1)
       
    def __str__(self):
        return self.id
        
    def fullname(self):
        return self.lastname +', '+self.firstname+' '+self.middlename+' '+self.name_extension
        
    def get_age(self):
    
        bd                      = self.birthdate

        array_bdate             = bd.split('-')
        year                    = int(array_bdate[0])
        month                   = int(array_bdate[1])
        day                     = int(array_bdate[2])
        
        month_now               = int(datetime.datetime.now().strftime('%m'))
        day_now                 = int(datetime.datetime.now().strftime('%d'))

        date_diff               = datetime.date.today() - datetime.date(year, month, day)
        age                     = date_diff.total_seconds() / 60 / 60 / 24 / 365

        if(month_now >= month):
            if(month_now == month):
                if(day_now >= day):

                    age = math.ceil(age)
                    
                else:

                    age = math.floor(age)
                
            else:

                age = math.ceil(age)

        else: 

            age = math.floor(age)
            
        return age
        
class CourseEnrolled(models.Model):

    id = models.CharField(max_length = 125, default = 'C1', primary_key = True)
    course_id = models.CharField(max_length = 125, default = 'CID1')
    user_id = models.CharField(max_length = 125, default = 'AA1')
    datetime_applied = models.CharField(max_length = 30, default = 'September 11, 2021 | 1:00 PM')
    datetime_enrolled = models.CharField(max_length = 30, default = 'September 12, 2021 | 1:00 PM')
    enrolment_processed_by = models.CharField(max_length = 125, default = 'ADMIN1')
    hours_duration = models.CharField(max_length = 5, default = '400')
    status = models.CharField(max_length = 1,default = '0')
        
    def __str__(self):
        return self.id
