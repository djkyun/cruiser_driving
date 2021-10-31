from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import LoginHistory, Course, SystemSettings, Category, PaymentMethodList, Enrolment, SalesTransaction, Appointment, TimeScheduleAppointment, ScheduleType, Attendance, Rooms, Lesson, LessonDetailTitle, LessonDetail, InstructorSpecialization, CategoryType, CarType
from website.models import UserRecords
from django.db.models import Q, Sum, Avg
from django.contrib.auth.models import User
from django.contrib.auth import login as login_form, authenticate, logout as logout_form
from django.contrib import messages
from .forms import SystemSettingsForm
from itertools import chain
import datetime, math
import pytz
import random

# Create your views here.

url_base = '127.0.0.1:8000/'
url_base = '127.0.0.1:8000/'
website_name = 'Cruiser Driving School'
total_number_applicants = UserRecords.objects.filter(role_id = '1').count()
total_number_students =  UserRecords.objects.filter(role_id = '2').count()
total_number_completed_students =  Enrolment.objects.filter(status = '1').count()
average_number_students_per_course = len(UserRecords.objects.all())
average_age_students = len(UserRecords.objects.all())
enrolled_hours_ratio = len(UserRecords.objects.all())

def login_admin(request):
    
    menu_name = 'Admin Login'
    
    if(request.method == "POST"):
    
        username_input = request.POST['username']
        password_input = request.POST['password']
        
        user_credential_info = authenticate(username = username_input, password = password_input)
               
        
        if user_credential_info is not None:
        
           userlist = UserRecords.objects.all()
           students_list = UserRecords.objects.filter(role_id = '2')
           
           login_form(request, user_credential_info)   
           
           if user_credential_info.is_superuser == 1:
           
               return render(
               
                   request,   
                   'admin_page/index.html',
                       {
                            'website_name': website_name,
                            'menu_name':'Home',
                            'username': username_input,
                            'userlist': userlist,
                            'students_list': students_list,
                            'url_base': url_base,
                            'total_number_applicants': total_number_applicants,
                            'total_number_students': total_number_students,
                            'total_number_completed_students': total_number_completed_students,
                            'average_number_students_per_course': average_number_students_per_course,
                            'average_age_students': average_age_students,
                            'enrolled_hours_ratio': enrolled_hours_ratio
                       }
               
               )
           
           else:
            
                messages.error(request,"You are not allowed to access Admin Page")
             
                return render(
                    request,
                    'admin_page/login.html',                
                    {
                        'website_name':website_name,
                        'menu_name': menu_name
                    }
                )   
           
            
        else:            
            
            messages.error(request,"User credential not found or invalid password")
             
            return render(
                request,
                'admin_page/login.html',                
                {
                    'website_name':website_name,
                    'menu_name': menu_name
                }
            )
            
           
    
    else:
    
        return HttpResponse('request not allowed')
    

def dashboard(request):
        
   userlist             = UserRecords.objects.filter(role_id = '2')
   enrolment_list       = Enrolment.objects.all()
   courselist           = Course.objects.all()
   
  
   
   if request.user.is_authenticated:
         username = request.user
   else:
        return redirect('/')  
    
   return render(
   
   request,   
   'admin_page/index.html',
       {
            'website_name': website_name,
            'menu_name':'Home',
            'username': username,
            'userlist': userlist,
            'enrolment_list': enrolment_list,
            'courselist': courselist,
            'url_base': url_base,
            'total_number_applicants': total_number_applicants,
            'total_number_students': total_number_students,
            'total_number_completed_students': total_number_completed_students,          
            'average_age_students': average_age_students,
            'enrolled_hours_ratio': enrolled_hours_ratio
       }
   
   )
    
def applicants(request):
   
    if request.user.is_authenticated:
         username = request.user
         user_id = username.id
    else:
        return redirect('/admin_page')  
        
    categorylist                        = Category.objects.all()
    courselist                          = Course.objects.all().order_by('id') 
    userlist                            = UserRecords.objects.filter(role_id = '1')
    instructor_list                     = UserRecords.objects.filter(role_id = '3')
    enrolment_list                      = Enrolment.objects.all().order_by('id')
    paymentmethod_list                  = PaymentMethodList.objects.all().order_by('id') 
    sales_transaction_list              = SalesTransaction.objects.all()
    appointment_list                    = Appointment.objects.all()
    attendance_list                     = Attendance.objects.all()
    schedule_type_list                  = ScheduleType.objects.all().order_by('id')
    categorytypelist                    = CategoryType.objects.all()
    cartypelist                         = CarType.objects.all()
    timescheduleappointment_list        = TimeScheduleAppointment.objects.all()
    
    User_list                           = User.objects.all()
    
    return render(
        request,
        'admin_page/applicants.html',
        {
            'website_name': website_name,
            'userlist': userlist,
            'instructor_list': instructor_list,
            'User_list': User_list,
            'courselist': courselist,
            'categorylist': categorylist, 
            'categorytypelist': categorytypelist,              
            'cartypelist': cartypelist,              
            'enrolment_list': enrolment_list,
            'attendance_list': attendance_list,
            'appointment_list': appointment_list,
            'schedule_type_list': schedule_type_list,
            'paymentmethod_list': paymentmethod_list,
            'sales_transaction_list': sales_transaction_list,
            'timescheduleappointment': timescheduleappointment_list,
            'username': username,
            'user_id': user_id,
            'menu_name':'Applicants',
            'get_category_id':get_category_id(10),
            'total_number_applicants': total_number_applicants,
            'total_number_students': total_number_students,
            'total_number_completed_students': total_number_completed_students,
            'average_number_students_per_course': average_number_students_per_course,
            'average_age_students': average_age_students,
            'enrolled_hours_ratio': enrolled_hours_ratio
        }
    )

def enroll_student(request):

    processed_by                                = request.POST['admin_id']
    time_schedule_appointment_id                = request.POST['time_schedule_appointment_id']
    enrolment_id                                = request.POST['enrolment_id']
    authentication_user_id                      = request.POST['authentication_user_id']
    schedule                                    = request.POST['schedule']
    
    enrolment_record                            = Enrolment.objects.get(id = enrolment_id)
    enrolment_record.status                     = '1'   
    enrolment_record.save()
    
    user_record                                 = UserRecords.objects.get(authentication_user_id = authentication_user_id)
    user_record.role_id                         = '2'
    user_record.save()
    
    course_hours                                = request.POST['course_hours']
    appointment_hours_per_day                   = request.POST['appointment_hours_per_day']
    
    course_hours_int                            = int(course_hours)
    hours_per_day_int                           = int(appointment_hours_per_day)
    
    excess_duration                             = course_hours_int % hours_per_day_int
    days_duration                               = course_hours_int / hours_per_day_int
    
    scheduled_days                              = []
    
    scheduled_days                              = schedule.split('-')
    
    scheduled_days_count                        = len(scheduled_days)
    
   

    if excess_duration > 0:       
        days_duration = int(days_duration) + 1
        
    for i in range(1, int(days_duration)):
    
        days_duration = int(days_duration)
    
        if str(i) == str(days_duration) and excess_duration > 0:
            hours_per_day = int(excess_duration)
        else:
            hours_per_day = hours_per_day_int
            
        if days_duration > scheduled_days_count:
        
            index_day = days_duration % scheduled_days_count
            
            if index_day < 1:
                index_day = days_duration - schedule_days_count
                
            ndx = index_day - 1
            scheduled_day_string = scheduled_days[ndx]
            
        else:
            ndx = i - 1
            scheduled_day_string = scheduled_days[ndx]
    
        attendance_record = Attendance(
            time_schedule_appointment_id = time_schedule_appointment_id,
            enrolment_id = enrolment_id,
            status = '0',           
            hours_rendered = hours_per_day
        )
        
        attendance_record.save()
    
    messages.success(request, "1 Student Enrolled!")
    
    return redirect('students_admin')
    #return HttpResponse(excess_duration)
    
def applicants_print(request):
    
    if request.user.is_authenticated:
         username = request.user
    else:
        return redirect('/admin_page')
    
    categorylist                = Category.objects.all()
    courselist                  = Course.objects.all().order_by('id') 
    userlist                    = UserRecords.objects.all().order_by('lastname') 
    enrolment_list              = Enrolment.objects.all().order_by('id')
    paymentmethod_list          = PaymentMethodList.objects.all().order_by('id') 
    sales_transaction_list      = SalesTransaction.objects.all()

    context = {
        
        'menu_page':'Print',
        'print_title':'Applicants List as of ' + str(datetime.datetime.now()),
        'userlist': userlist,
        'courselist': courselist,
        'categorylist': categorylist,            
        'enrolment_list': enrolment_list,
        'paymentmethod_list': paymentmethod_list,
        'sales_transaction_list': sales_transaction_list
        
    }
    
    return render(request, 'admin_page/applicants_print.html', context)
    
def get_category_id(name_here):

    value_var = name_here * 10
    return value_var
    
def declare_payment(request):

    if request.user.is_authenticated:
         username = request.user
         admin_user_id = username.id
    else:
        return redirect('/')  
        
    enrolment_id                            = request.POST['enrolment_id']
    amount_paid                             = request.POST['amount_paid']
    payment_method_id                       = request.POST['payment_method']
    for_payment_term                        = request.POST['for_payment_term']      
    applicant_user_id                       = request.POST['applicant_user_id']
    
  
  
    
    amount_balance                          = 0
    
    if str(for_payment_term) == "2": 
        amount_balance                      = 0
    if str(for_payment_term) == "1":     
        enrolment_list                      = Enrolment.objects.get(id = enrolment_id)         
        amount_balance                      = float(enrolment_list.amount) - float(amount_paid)

    if payment_method_id != '3':
    
        sales_transaction                   = SalesTransaction.objects.get(enrolment_id = enrolment_id, for_payment_term = for_payment_term)
        sales_transaction.status            = 1
        sales_transaction.amount_balance    = amount_balance
        sales_transaction.amount_paid       = amount_paid
        sales_transaction.for_payment_term  = for_payment_term
        sales_transaction.save()

        messages.success(request, "Payment Successfully Declared!")     

    else:           
        
        cash_reference_number                   = request.POST['cash_reference_number']   
         
        sales_transaction = SalesTransaction(
            user_id = applicant_user_id,
            enrolment_id = enrolment_id,
            amount_paid = amount_paid,
            amount_balance = amount_balance,
            payment_method = payment_method_id,
            payment_reference_no = cash_reference_number,
            transaction_type = '1',
            for_payment_term = for_payment_term,
            payment_term = for_payment_term,
            processed_by = admin_user_id,
            status = 1
        )
        
        sales_transaction.save()
        
        messages.success(request, "Payment Successfully Declared!")
        
    
    return redirect('applicants')
    
def students_admin(request):
   
    userlist                        = UserRecords.objects.all()
    instructor_list                 = UserRecords.objects.filter(role_id = '3')
    student_list                    = UserRecords.objects.filter(role_id = '2')
    student_list_completed          = UserRecords.objects.filter(role_id = '2')
    appointment_list                = Appointment.objects.all()
    attendance_list                 = Attendance.objects.all()
    enrolmentlist                   = Enrolment.objects.all()
    sales_transaction_list          = SalesTransaction.objects.all().order_by('id')
    courselist                      = Course.objects.all()
    categorylist                    = Category.objects.all()
    schedule_type_list              = ScheduleType.objects.all().order_by('id') 
    categorytypelist                = CategoryType.objects.all().order_by('id') 
    cartypelist                     = CarType.objects.all().order_by('id') 
    
    if request.user.is_authenticated:
         username = request.user
    else:
        return redirect('/')  
     
    return render(
        request,
        'admin_page/students.html',
        {
            'website_name': website_name,
            'userlist': userlist,
            'student_list': student_list,
            'instructor_list': instructor_list,
            'student_list_completed': student_list_completed,
            'attendance_list': attendance_list,
            'schedule_type_list': schedule_type_list,
            'appointment_list': appointment_list,
            'sales_transaction_list': sales_transaction_list,
            'enrolmentlist': enrolmentlist,
            'courselist':courselist,
            'categorylist':categorylist,
            'categorytypelist':categorytypelist,
            'cartypelist':cartypelist,
            'username': username,
            'student_counts': total_number_students,
            'menu_name':'Students List'
        }
    )
    
def instructors(request):
   
    userlist                        = UserRecords.objects.filter(role_id = 3).order_by('lastname') 
    user_account_list               = User.objects.all()
    courselist                      = Course.objects.all()
    instructor_specialization_list  = InstructorSpecialization.objects.all()
    instructor_count                = len(userlist)
    
    if request.user.is_authenticated:
    
        username = request.user
        user_id = username.id
        
        try:
            user_list = UserRecords.objects.get(authentication_user_id = user_id)
            fullname = user_list.firstname +' '+user_list.lastname  
        except:
            user_list = ''
            fullname = ''
            
    else:
        return redirect('/')  
     
    return render(
        request,
        'admin_page/instructors.html',
        {
            'website_name': website_name,
            'username': username,
            'fullname': fullname,
            'courselist': courselist,
            'user_account_list': user_account_list,
            'instructor_specialization_list': instructor_specialization_list,
            'userlist': userlist,
            'instructor_count': instructor_count,
            'menu_name':'Instructors'
        }
    )
    
def add_instructor(request):

    firstname                       = request.POST['firstname']
    middlename                      = request.POST['middlename']
    lastname                        = request.POST['lastname']
    name_extension                  = request.POST['name_extension']
    
    complete_address                = request.POST['complete_address']
    email_address                   = request.POST['email_address']
    contact_number                  = request.POST['contact_number']
    complete_address                = request.POST['complete_address']
    
    civil_status                    = request.POST['civil_status']
    gender                          = request.POST['gender']
    birthdate                       = request.POST['birthdate']
    
    username                        = request.POST['username']
    password                        = request.POST['password']
    retry_password                  = request.POST['retry_password']
    
    user_records = User.objects.create_user(
        username = username,
        email = email_address,
        password = password,
        first_name = firstname,
        last_name = lastname,
        is_active = True
    )
        
    user_records.save()
    
    user_records_filter             = User.objects.get(email = email_address)
    inserted_id                     = user_records_filter.id
                    
    user_information = UserRecords(
        authentication_user_id      = inserted_id,
        firstname                   = firstname,
        lastname                    = lastname,
        middlename                  = middlename,
        name_extension              = name_extension,
        birthdate                   = birthdate,       
        complete_address            = complete_address,
        email_address               = email_address,
        contact_number              = contact_number,
        gender                      = gender,
        role_id                     = 3,
        civil_status                = civil_status
    )
    
    user_information.save()
    
    messages.success(request,"1 Instructor Record Added!")
    
    return redirect('instructors')
    
def add_specialization(request):

    if request.user.is_authenticated:
    
        username = request.user
        user_id = username.id
        
        try:
            user_list = UserRecords.objects.get(authentication_user_id = user_id)
            fullname = user_list.firstname +' '+user_list.lastname  
        except:
            user_list = ''
            fullname = ''   
        
    else:
        return redirect('/') 
        
    instructor_id               = request.POST['instructor_id']   
    instructor_fullname         = request.POST['instructor_fullname']
    course_specialization       = request.POST.getlist('course_specialization')
    
    course_count                = len(course_specialization)
    
    if course_count > 0:
    
        for i in course_specialization:  
            instructor_specialization_record = InstructorSpecialization(
                instructor_id = instructor_id,
                course_id = i,
                assigned_by = user_id
            )
            
            instructor_specialization_record.save()
    
    else:
    
        messages.error(request," No course specialization added to "+ instructor_fullname)

   
    
    messages.success(request,"Specialization Added to "+ instructor_fullname)

    return redirect('instructors')
    
def remove_specialization(request):

    if request.user.is_authenticated:
    
        username = request.user
        user_id = username.id
        
        try:
            user_list = UserRecords.objects.get(authentication_user_id = user_id)
            fullname = user_list.firstname +' '+user_list.lastname  
        except:
            user_list = ''
            fullname = ''   
        
    else:
        return redirect('/') 
        
    specialization_id           = request.POST['specialization_id']   
    instructor_fullname         = request.POST['instructor_fullname']
    course_specialization       = request.POST['specialization_details']
    
    specialization_record = InstructorSpecialization.objects.get(instructor_specs_id = specialization_id)
    specialization_record.delete()
      
    messages.success(request,"Specialization Removed from "+ instructor_fullname + ' ' + course_specialization)

    return redirect('instructors')
    
def admin_accounts(request):
   
    userlist                = UserRecords.objects.all().order_by('lastname') 
    cartypelist             = CarType.objects.all()
    categorytypelist        = CategoryType.objects.all()
    
    if request.user.is_authenticated:
    
        username = request.user
        user_id = username.id
        
        try:
            user_list = UserRecords.objects.get(authentication_user_id = user_id)
            fullname = user_list.firstname +' '+user_list.lastname  
        except:
            user_list = ''
            fullname = ''   
        
    else:
        return redirect('/') 
     
    return render(
        request,
        'admin_page/admin_accounts.html',
        {
            'website_name': website_name,
            'userlist': userlist,
            'cartypelist': userlist,
            'categorytypelist': userlist,
            'userlist': username,
            'fullname': fullname,
            'menu_name':'Admin Accounts'
        }
    )
    
def skills_assessments(request):
   
          
    categorylist                = Category.objects.all()
    categorytypelist            = CategoryType.objects.all()
    cartypelist                 = CarType.objects.all()
    courselist                  = Course.objects.all().order_by('id') 
    userlist                    = UserRecords.objects.filter(role_id = '2')
    enrolment_list              = Enrolment.objects.all().order_by('id')
      
    if request.user.is_authenticated:
    
        username = request.user
        user_id = username.id
        
        try:
            user_list = UserRecords.objects.get(authentication_user_id = user_id)
            fullname = user_list.firstname +' '+user_list.lastname
        except:
            user_list = ''
            fullname = ''
        
    else:
        return redirect('/')   
        
    return render(
        request,
        'admin_page/skills_assessments.html',
        {
            'website_name': website_name,
            'userlist': userlist,
            'courselist': courselist,
            'categorylist': categorylist,            
            'categorytypelist': categorytypelist,            
            'cartypelist': cartypelist,            
            'enrolment_list': enrolment_list,
            'username': username,
            'fullname': fullname,
            'menu_name':'Skills Assessments'
        }
    )
    
    
def lessons_admin(request):
   
    if request.user.is_authenticated:
         username = request.user
         user_id = username.id
    else:
        return redirect('/admin_page')  
        
    lesson_list                 = Lesson.objects.all()
    categorylist                = Category.objects.all()
    categorytypelist            = CategoryType.objects.all()
    cartypelist                 = CarType.objects.all()
    courselist                  = Course.objects.all().order_by('id') 
    userlist                    = UserRecords.objects.filter(role_id = '1')
    instructor_list             = UserRecords.objects.filter(role_id = '3')
    enrolment_list              = Enrolment.objects.all().order_by('id')
    paymentmethod_list          = PaymentMethodList.objects.all().order_by('id') 
    sales_transaction_list      = SalesTransaction.objects.all()
    appointment_list            = Appointment.objects.all()
    attendance_list             = Attendance.objects.all()
    schedule_type_list          = ScheduleType.objects.all().order_by('id') 
    
    User_list                   = User.objects.all()
    
    return render(
        request,
        'admin_page/lessons.html',
        {
            'website_name': website_name,
            'userlist': userlist,
            'instructor_list': instructor_list,
            'User_list': User_list,
            'lesson_list': lesson_list,
            'courselist': courselist,
            'categorylist': categorylist,            
            'categorytypelist': categorytypelist,            
            'cartypelist': cartypelist,            
            'enrolment_list': enrolment_list,
            'attendance_list': attendance_list,
            'appointment_list': appointment_list,
            'schedule_type_list': schedule_type_list,
            'paymentmethod_list': paymentmethod_list,
            'sales_transaction_list': sales_transaction_list,
            'username': username,
            'user_id': user_id,
            'menu_name':'Applicants',
            'get_category_id':get_category_id(10),
            'total_number_applicants': total_number_applicants,
            'total_number_students': total_number_students,
            'total_number_completed_students': total_number_completed_students,
            'average_number_students_per_course': average_number_students_per_course,
            'average_age_students': average_age_students,
            'enrolled_hours_ratio': enrolled_hours_ratio
        }
    )
    
def add_lesson(request):
   
    if request.user.is_authenticated:
        username = request.user
        user_id = username.id
    else:
        return redirect('/admin_page') 


    if(request.method == "POST"):

        course_id_input = request.POST['course_id']
        lesson_number_input = int(request.POST['number_of_lessons'])
        
        
        for ii in range(1,lesson_number_input):
        
            lesson_record = Lesson(
                course_id = course_id_input,
                lesson_number = str(ii)
            )
            
            lesson_record.save()
            
        messages.success(request,"Lesson Numbers Added, You may now add Lesson Details for every Lesson Number")
        
        
    categorylist                = Category.objects.all()
    categorytypelist            = CategoryType.objects.all()
    cartypelist                 = CarType.objects.all()
    courselist                  = Course.objects.all().order_by('id') 
    userlist                    = UserRecords.objects.filter(role_id = '1')
    instructor_list             = UserRecords.objects.filter(role_id = '3')
    enrolment_list              = Enrolment.objects.all().order_by('id')
    paymentmethod_list          = PaymentMethodList.objects.all().order_by('id') 
    sales_transaction_list      = SalesTransaction.objects.all()
    appointment_list            = Appointment.objects.all()
    attendance_list             = Attendance.objects.all()
    schedule_type_list          = ScheduleType.objects.all().order_by('id') 

    User_list                   = User.objects.all()

    return render(
        request,
        'admin_page/lessons.html',
        {
            'website_name': website_name,
            'userlist': userlist,
            'instructor_list': instructor_list,
            'User_list': User_list,
            'courselist': courselist,
            'categorylist': categorylist,            
            'categorytypelist': categorytypelist,            
            'cartypelist': cartypelist,            
            'enrolment_list': enrolment_list,
            'attendance_list': attendance_list,
            'appointment_list': appointment_list,
            'schedule_type_list': schedule_type_list,
            'paymentmethod_list': paymentmethod_list,
            'sales_transaction_list': sales_transaction_list,
            'username': username,
            'user_id': user_id,
            'menu_name':'Applicants',
            'get_category_id':get_category_id(10),
            'total_number_applicants': total_number_applicants,
            'total_number_students': total_number_students,
            'total_number_completed_students': total_number_completed_students,
            'average_number_students_per_course': average_number_students_per_course,
            'average_age_students': average_age_students,
            'enrolled_hours_ratio': enrolled_hours_ratio
        }
    )

def add_lesson_detail(request):
   
    if request.user.is_authenticated:
        username = request.user
        user_id = username.id
    else:
        return redirect('/admin_page') 


    if(request.method == "POST"):

        course_details = request.POST['course_details']
        lesson_id_input = request.POST['lesson_id']
        lesson_detail_input = request.POST['lesson_detail']
        
        lesson_detail_records = LessonDetail(
            lesson_id = lesson_id_input,
            lesson_detail = lesson_detail_input
        )
      
        lesson_detail_records.save()
        
        added_details = course_details + " for lesson number " + lesson_id_input
            
        messages.success(request,"Lesson Detail Added to " + added_details + "")
        
        
    categorylist                = Category.objects.all()
    categorytypelist            = CategoryType.objects.all()
    cartypelist                 = CarType.objects.all()
    courselist                  = Course.objects.all().order_by('id') 
    userlist                    = UserRecords.objects.filter(role_id = '1')
    instructor_list             = UserRecords.objects.filter(role_id = '3')
    enrolment_list              = Enrolment.objects.all().order_by('id')
    paymentmethod_list          = PaymentMethodList.objects.all().order_by('id') 
    sales_transaction_list      = SalesTransaction.objects.all()
    appointment_list            = Appointment.objects.all()
    attendance_list             = Attendance.objects.all()
    schedule_type_list          = ScheduleType.objects.all().order_by('id') 

    User_list                   = User.objects.all()

    return render(
        request,
        'admin_page/lessons.html',
        {
            'website_name': website_name,
            'userlist': userlist,
            'instructor_list': instructor_list,
            'User_list': User_list,
            'courselist': courselist,
            'categorylist': categorylist,            
            'categorytypelist': categorytypelist,            
            'cartypelist': cartypelist,            
            'enrolment_list': enrolment_list,
            'attendance_list': attendance_list,
            'appointment_list': appointment_list,
            'schedule_type_list': schedule_type_list,
            'paymentmethod_list': paymentmethod_list,
            'sales_transaction_list': sales_transaction_list,
            'username': username,
            'user_id': user_id,
            'menu_name':'Applicants',
            'get_category_id':get_category_id(10),
            'total_number_applicants': total_number_applicants,
            'total_number_students': total_number_students,
            'total_number_completed_students': total_number_completed_students,
            'average_number_students_per_course': average_number_students_per_course,
            'average_age_students': average_age_students,
            'enrolled_hours_ratio': enrolled_hours_ratio
        }
    )
    
def appointments_admin(request):
   
    userlist                = UserRecords.objects.all().order_by('lastname') 
    instructor_list         = UserRecords.objects.filter(role_id = '3')
    enrolment_list          = Enrolment.objects.all().order_by('id') 
    course_list             = Course.objects.all().order_by('id') 
    attendance_list         = Attendance.objects.all().order_by('id') 
    appointment_list        = Appointment.objects.all().order_by('id') 
    timeschedule_list       = TimeScheduleAppointment.objects.all().order_by('id') 
    rooms_list              = Rooms.objects.all().order_by('id') 
    scheduled_type_list     = ScheduleType.objects.all().order_by('id') 
    
    if request.user.is_authenticated:
    
        username = request.user
        user_id = username.id
        
        try:
            user_list = UserRecords.objects.get(authentication_user_id = user_id)
            fullname = user_list.firstname +' '+user_list.lastname  
        except:
            user_list = ''
            fullname = ''
            
    else:
        return redirect('/')  
       
    return render(
        request,
        'admin_page/appointments.html',
        {
            'website_name': website_name,
            'userlist': userlist,
            'instructor_list': instructor_list,
            'scheduled_type_list': scheduled_type_list,
            'user_id': user_id,
            'course_list': course_list,
            'appointment_list': appointment_list,
            'rooms_list': rooms_list,         
            'attendance_list': attendance_list,
            'enrolment_list': enrolment_list,
            'timeschedule_list':timeschedule_list,
            'username': username,
            'fullname': fullname,
            'menu_name':'Appointments'
        }
    )

def add_appointment(request):

    if request.user.is_authenticated:
    
        username = request.user
        user_id = username.id
        
        try:
            user_list = UserRecords.objects.get(authentication_user_id = user_id)
            fullname = user_list.firstname +' '+user_list.lastname  
        except:
            user_list = ''
            fullname = ''
            
    else:
        return redirect('/')
        
    batch_appointment_code      = request.POST['batch_appointment_code']
    batch_appointment_name      = request.POST['batch_appointment_name']
    schedule_type_id            = request.POST['schedule_type_id']   
    admin_id                    = request.POST['admin_id']
    
    appointment_record = Appointment(
        batch_appointment_code = batch_appointment_code,
        batch_appointment_name = batch_appointment_name,
        schedule_type = schedule_type_id,      
        processed_by = admin_id
    )
    
    appointment_record.save()
    
    messages.success(request,"1 Appointment Added")
    return redirect('appointments_admin')
    
def add_timeschedule_appointment(request):

    if request.user.is_authenticated:
    
        username = request.user
        user_id = username.id
        
        try:
            user_list = UserRecords.objects.get(authentication_user_id = user_id)
            fullname = user_list.firstname +' '+user_list.lastname  
        except:
            user_list = ''
            fullname = ''
            
    else:
        return redirect('/')
        
    instructor_id                       = request.POST['instructor_id']     
    course_id                           = request.POST['course_id']     
    scheduled_day                       = request.POST.getlist('scheduled_days')
    time_start                          = request.POST['time_start']     
    time_end                            = request.POST['time_end']
    room_id                             = request.POST['room_id']
    assigned_by                         = user_id  
    appointment_id                      = request.POST['appointment_id']
    
    for i in scheduled_day:

        chosen_scheduled_day            = i
    
        time_schedule_record            = TimeScheduleAppointment(
            instructor_id               = instructor_id,
            course_id                   = course_id,
            scheduled_day               = chosen_scheduled_day,
            time_start                  = time_start,
            time_end                    = time_end,
            room_id                     = room_id,
            assigned_by                 = assigned_by,
            appointment_id              = appointment_id
        )
        
        time_schedule_record.save()
    
    
    messages.success(request, "1 Time Schedule Added")
    
    return redirect('appointments_admin')
 
def schedule_types(request):
   
   
    user_list           = User.objects.all().order_by('id') 
    userlist            = UserRecords.objects.all().order_by('lastname') 
    appointment_list    = Appointment.objects.all().order_by('id') 
    schedule_type_list  = ScheduleType.objects.all().order_by('id') 
    
    if request.user.is_authenticated:
    
        username = request.user
        user_id = username.id
        
        try:
            user_list = UserRecords.objects.get(authentication_user_id = user_id)
            fullname = user_list.firstname +' '+user_list.lastname  
        except:
            user_list = ''
            fullname = ''
            
    else:
        return redirect('/')  
       
    return render(
        request,
        'admin_page/schedule_types.html',
        {
            'website_name': website_name,
            'user_list': user_list,
            'userlist': userlist,
            'user_id': user_id,
            'appointment_list': appointment_list,
            'schedule_type_list': schedule_type_list,
            'username': username,
            'fullname': fullname,
            'menu_name':'Appointments'
        }
    )
    
def add_schedule_type(request):
    
    if request.user.is_authenticated:
    
        username = request.user
        user_id = username.id
            
    else:
        return redirect('/')  
        
    hours_per_day = request.POST['hours_per_day']
    days_array = request.POST.getlist('scheduled_day')
    
    days_len = len(days_array)
    
    string_value = ''
    
    if days_len > 0:    

        for i in days_array:
            string_value = string_value + i + '-'
            
        len_string = len(string_value) - 1
        string_value = string_value[0:len_string]       

        schedule_type_record = ScheduleType(
            schedules = string_value,
            hours_per_day = hours_per_day,
            status = '1',
            added_by = user_id        
        )

        schedule_type_record.save()

        message_display = "1 Schedule Type Added " + string_value    
        messages.success(request,message_display)

    else:
        message_display = "Please Specify Days of Schedules (e.g. Monday, Tuesday etc.)"
        messages.error(request,message_display)     
   
    return redirect('schedule_types')

 
def course_details(request):
    
    if request.method == "POST":
    
        operation = request.POST['operation']
        
        if operation == "edit":
        
            course_id = request.POST['course_id']
        
            course_code_edit                    = request.POST['course_code_edit']
            course_name_edit                    = request.POST['course_name_edit']
            course_description_edit             = request.POST['course_description_edit']
            hours_duration_edit                 = request.POST['hours_duration_edit']
            tuition_fee_edit                    = request.POST['tuition_fee_edit']
            category_id_edit                    = request.POST['category_id_edit']
            car_type_id_edit                    = request.POST['car_type_id_edit']
        
            course_detail                       = Course.objects.get(id = course_id)
            course_detail.course_code           = course_code_edit  
            course_detail.course_name           = course_name_edit  
            course_detail.course_description    = course_description_edit  
            course_detail.hours_duration        = hours_duration_edit  
            course_detail.category_id           = category_id_edit  
            course_detail.car_type_id           = car_type_id_edit  
            course_detail.tuition_fee           = tuition_fee_edit 
            course_detail.save()
            
            messages.success(request, "Successfully updated 1 record "+course_name_edit)
            
  
    auth_userlist = User.objects.all().order_by('id') 
    userlist = UserRecords.objects.all().order_by('id') 
    courselist = Course.objects.all().order_by('id') 
    categorylist = Category.objects.all().order_by('id') 
    categorytypelist = CategoryType.objects.all().order_by('id') 
    cartypelist = CarType.objects.all().order_by('id') 
   
    #datetime_now = datetime.now()
    #datetime_now_formatted = datetime_now.strftime('%m-%d-%Y %h-%M-%s')
    datetime_now_formatted = '9-12-2021 14:30:45'
   
    if request.user.is_authenticated:
    
        username = request.user
        user_id = username.id
        
        try:
            user_list = UserRecords.objects.get(authentication_user_id = user_id)
            fullname = user_list.firstname +' '+user_list.lastname  
        except:
            user_list = ''
            fullname = ''
        
    else:
        return redirect('/') 
    
   
    context = {
   
        'website_name': website_name,
        'menu_name':'Home',
        'username': username,
        'fullname': fullname,
        'datetime_now': datetime_now_formatted,        
        'courselist': courselist,
        'categorylist': categorylist,
        'categorytypelist': categorytypelist,
        'cartypelist': cartypelist,
        'auth_userlist': auth_userlist,
        'userlist': userlist,
        'url_base': url_base,
        'total_number_applicants': total_number_applicants
    }   
  
   
    return render(request,'admin_page/course_details.html', context)
    
    
def rooms(request):
    
    if request.method == "POST":
    
        operation = request.POST['operation']
        
        if operation == "edit":
        
            course_id = request.POST['course_id']
        
            course_code_edit                    = request.POST['course_code_edit']
            course_name_edit                    = request.POST['course_name_edit']
            course_description_edit             = request.POST['course_description_edit']
            hours_duration_edit                 = request.POST['hours_duration_edit']
            category_id_edit                    = request.POST['category_id_edit']
            car_type_id_edit                    = request.POST['car_type_id_edit']
        
            course_detail                       = Course.objects.get(id = course_id)
            course_detail.course_code           = course_code_edit  
            course_detail.course_name           = course_name_edit  
            course_detail.course_description    = course_description_edit  
            course_detail.hours_duration        = hours_duration_edit  
            course_detail.category_id           = category_id_edit  
            course_detail.car_type_id           = car_type_id_edit  
            course_detail.save()
            
            messages.success(request, "Successfully updated 1 record "+course_name_edit)
            
  
    auth_userlist               = User.objects.all().order_by('id') 
    userlist                    = UserRecords.objects.all().order_by('id') 
    courselist                  = Course.objects.all().order_by('id')  
    rooms_list                  = Rooms.objects.all()
  
   
    #datetime_now = datetime.now()
    #datetime_now_formatted = datetime_now.strftime('%m-%d-%Y %h-%M-%s')
    datetime_now_formatted = '9-12-2021 14:30:45'
   
    if request.user.is_authenticated:
    
        username = request.user
        user_id = username.id
        
        try:
            user_list = UserRecords.objects.get(authentication_user_id = user_id)
            fullname = user_list.firstname +' '+user_list.lastname  
        except:
            user_list = ''
            fullname = ''
        
    else:
        return redirect('/') 
    
   
    context = {
   
        'website_name': website_name,
        'menu_name':'Home',
        'username': username,
        'fullname': fullname,
        'datetime_now': datetime_now_formatted,  
        'auth_userlist': auth_userlist,
        'rooms_list': rooms_list,      
        'userlist': userlist,
        'url_base': url_base,
        'total_number_applicants': total_number_applicants
    }   
  
   
    return render(request,'admin_page/rooms.html', context)   

def add_room(request):
    
    if request.user.is_authenticated:
    
        username = request.user
        user_id = username.id
        
        try:
            user_list = UserRecords.objects.get(authentication_user_id = user_id)
            fullname = user_list.firstname +' '+user_list.lastname  
        except:
            user_list = ''
            fullname = ''
        
    else:
        return redirect('/')
        
    room_name       = request.POST['room_name']
    room_no         = request.POST['room_no']
    building        = request.POST['building']
    floor           = request.POST['floor']

    room_list = Rooms(
        room_name   = room_name,
        room_no     = room_no,
        building    = building,
        floor       = floor,
        status      = '1',
        added_by    = user_id,
        updated_by  = user_id
    )
    
    room_list.save()
    
    messages.success(request, "1 Room Added! "+room_name+' '+room_no+' ')

    return redirect('rooms')
   
def category_details_edit(request):

    if request.method == "POST":
    
        category_id                     = request.POST['id']
        category_name                   = request.POST['category_name_edit']
        
        category_detail                 = Category.objects.get(id = category_id)
        category_detail.category_name   = category_name
        
        category_detail.save()
        
        messages.success(request, "Successfully updated 1 record "+category_name)
        
    return redirect('course_details')
    
def category_type_details_edit(request):

    if request.method == "POST":
    
        category_type_id                             = request.POST['id']
        category_type_name                           = request.POST['category_type_name_edit']
        
        category_type_detail                         = CategoryType.objects.get(id = category_type_id)
        category_type_detail.category_type_name      = category_type_name
        
        category_type_detail.save()
        
        messages.success(request, "Successfully updated 1 record "+category_type_name)
        
    return redirect('course_details')
    

def car_type_edit(request):

    if request.method == "POST":
    
        car_type_id                     = request.POST['id']
        car_type_name                   = request.POST['car_type_name_edit']
        
        car_type_detail                 = CarType.objects.get(id = car_type_id)
        car_type_detail.car_type_name   = car_type_name
        
        car_type_detail.save()
        
        messages.success(request, "Successfully updated 1 record "+car_type_name)
        
    return redirect('course_details')
   
def add_course(request):

    if request.user.is_authenticated:
    
        username = request.user
        user_id = username.id
        
        try:
            user_list = UserRecords.objects.get(authentication_user_id = user_id)
            fullname = user_list.firstname +' '+user_list.lastname  
        except:
            user_list = ''
            fullname = ''
        
    else:
        return redirect('/') 
        
        
    course_code = request.POST['course_code']
    course_name = request.POST['course_name']
    course_description = request.POST['course_description']   
    tuition_fee = request.POST['tuition_fee']
    hours_duration = request.POST['hours_duration']    
    datetime_added = request.POST['datetime_added']
    category_id = request.POST['category_id']
    car_type_id = request.POST['car_type_id']
    
    added_by = user_id
    
    
    course_list = Course(
    
        course_code = course_code,
        course_name = course_name,
        course_description =  course_description,
        tuition_fee = tuition_fee,
        hours_duration =  hours_duration,
        added_by = added_by,
        datetime_added =  datetime_added,
        category_id = category_id,
        car_type_id = car_type_id
    
    )
    
    course_list.save()
    
    messages.success(request, "1 Course Added")
    
    return redirect('course_details')
    
def add_category(request):

    category_list = Category(
    
        category_name = request.POST['category_name']     
    
    )
    
    category_list.save()
    
    return redirect('course_details')
    
def add_category_type(request):

    if request.user.is_authenticated:
    
        username = request.user
        user_id = username.id
        
        try:
            user_list = UserRecords.objects.get(authentication_user_id = user_id)
            fullname = user_list.firstname +' '+user_list.lastname  
        except:
            user_list = ''
            fullname = ''
        
    else:
        return redirect('/') 
        
        
    list_record = CategoryType(
    
        category_type_name = request.POST['category_type_name'],
        added_by = user_id    
    
    )
    
    list_record.save()
    
    messages.success(request, "1 Category Type Added")
    
    return redirect('course_details')
    
def add_car_type(request):

    if request.user.is_authenticated:
    
        username = request.user
        user_id = username.id
        
        try:
            user_list = UserRecords.objects.get(authentication_user_id = user_id)
            fullname = user_list.firstname +' '+user_list.lastname  
        except:
            user_list = ''
            fullname = ''
        
    else:
        return redirect('/') 
        
        
    list_record_cartype = CarType(
    
        car_type_name = request.POST['car_type_name'],
        added_by = user_id    
    
    )
    
    list_record_cartype.save()
    
    messages.success(request, "1 Car Type Added")
    
    return redirect('course_details')
    
def add_category(request):

    category_name = request.POST['category_name']     
    category_type_id = request.POST['category_type_id']     

    category_list = Category(
    
        category_name = category_name,
        category_type_id = category_type_id
    )
    
    category_list.save()
    
    messages.success(request,"1 Category Added "+category_name)
    
    return redirect('course_details')
    
def enrolment_prediction(request):
   
    userlist = UserRecords.objects.all().order_by('lastname') 
    students_list = UserRecords.objects.filter(role_id = '2')
    courselist = Course.objects.all()
    categorylist = Category.objects.all()
    cartypelist = CarType.objects.all()
    categorytypelist = CategoryType.objects.all()
    enrolment_list = Enrolment.objects.all()
    
    #for_data_prediction = sorted(
        #chain(students_list,enrolment_list)        
    #)
    
    for_data_prediction = students_list
    
    data_prediction = for_data_prediction.only("firstname","lastname")
    
    if request.user.is_authenticated:
    
        username = request.user
        user_id = username.id
        
        try:
            user_list = UserRecords.objects.get(authentication_user_id = user_id)
            fullname = user_list.firstname +' '+user_list.lastname  
        except:
            user_list = ''
            fullname = ''
            
    else:
        return redirect('/')
    
     
    return render(
        request,
        'admin_page/enrolment_prediction.html',
        {
            'website_name': website_name,
            'for_data_prediction': for_data_prediction,
            'data_prediction': data_prediction,
            'userlist': userlist,
            'students_list': students_list,
            'courselist':courselist,
            'categorylist':categorylist,
            'categorytypelist':categorytypelist,
            'cartypelist':cartypelist,
            'enrolment_list':enrolment_list,
            'username': username,
            'fullname': fullname,
            'datetime_now': str(datetime.datetime.today()),
            'menu_name':'Enrolment Prediction'
        }
    )

def skills_assessment_reports(request):
   
    userlist = UserRecords.objects.all().order_by('lastname') 
    
    if request.user.is_authenticated:
    
        username = request.user
        user_id = username.id
        
        try:
            user_list = UserRecords.objects.get(authentication_user_id = user_id)
            fullname = user_list.firstname +' '+user_list.lastname  
        except:
            user_list = ''
            fullname = ''
     
    else:
        return redirect('/')
     
     
    return render(
        request,
        'admin_page/skills_assessment_reports.html',
        {
            'website_name': website_name,
            'userlist': userlist,
            'username': username,
            'fullname': fullname,
            'menu_name':'Skills Assessment Reports'
        }
    )
    
def insert_data(request):
   
    userlist = UserRecords.objects.all().order_by('lastname') 
    paymentmethod_list = PaymentMethodList.objects.all()
    
    if request.user.is_authenticated:
    
        username = request.user
        user_id = username.id
        
        try:
            user_list = UserRecords.objects.get(authentication_user_id = user_id)
            fullname = user_list.firstname +' '+user_list.lastname  
        except:
            user_list = ''
            fullname = ''
     
    else:
        return redirect('/')
     
     
    return render(
        request,
        'admin_page/insert_data.html',
        {
            'website_name': website_name,
            'userlist': userlist,
            'username': username,
            'fullname': fullname,
            'payment_method_list': paymentmethod_list,
            'menu_name':'Manual Insert Data'
        }
    )
    
def insert_data_process(request):
   
    userlist = UserRecords.objects.all().order_by('lastname') 
    paymentmethod_list = PaymentMethodList.objects.all()
    
    if request.user.is_authenticated:
    
        username = request.user
        user_id = username.id
        
        try:
            user_list = UserRecords.objects.get(authentication_user_id = user_id)
            fullname = user_list.firstname +' '+user_list.lastname  
        except:
            user_list = ''
            fullname = ''
     
    else:
        return redirect('/')
        
        if(request.method == "POST"):
        
            payment_method_input            = request.POST['payment_method']
            payment_method_image_input      = request.POST['payment_method_image']
            status_input                    = 1

            pml = PaymentMethodList(
                payment_method = payment_method_input,
                payment_method_image = payment_method_image_input,
                status = status_input
            )
            
            pml.save()

            messages.success(request, "Payment Method Saved!")
     
     
    return render(
        request,
        'admin_page/insert_data.html',
        {
            'website_name': website_name,
            'userlist': userlist,
            'username': username,
            'fullname': fullname,
            'payment_method_list': paymentmethod_list,
            'menu_name':'Manual Insert Data'
        }
    )
    
def delete_data(request):
   
    userlist = UserRecords.objects.all().order_by('lastname') 
    paymentmethod_list = PaymentMethodList.objects.all()
    courselist = Course.objects.all()
    
    if request.user.is_authenticated:
    
        username = request.user
        user_id = username.id
        
        try:
            user_list = UserRecords.objects.get(authentication_user_id = user_id)
            fullname = user_list.firstname +' '+user_list.lastname  
        except:
            user_list = ''
            fullname = ''
     
    else:
        return redirect('/')
     
     
    return render(
        request,
        'admin_page/delete_data.html',
        {
            'website_name': website_name,
            'userlist': userlist,
            'courselist': courselist,
            'username': username,
            'fullname': fullname,
            'payment_method_list': paymentmethod_list,
            'menu_name':'Manual Delete Data'
        }
    )
    
def delete_data_process(request):
   
    userlist = UserRecords.objects.all().order_by('lastname') 
    paymentmethod_list = PaymentMethodList.objects.all()
    
    if request.user.is_authenticated:
    
        username = request.user
        user_id = username.id
        
        try:
            user_list = UserRecords.objects.get(authentication_user_id = user_id)
            fullname = user_list.firstname +' '+user_list.lastname  
        except:
            user_list = ''
            fullname = ''
     
    else:
        return redirect('/')
        
        if(request.method == "POST"):
        
            course_id_input = request.POST['course_id']
            
            lesson_record = Lesson.objects.filter(course_id = course_id_input)
            lesson_record.delete()

            messages.success(request, "Course ID based from Lesson Deleted!")
     
     
    return render(
        request,
        'admin_page/delete_data.html',
        {
            'website_name': website_name,
            'userlist': userlist,
            'username': username,
            'fullname': fullname,
            'payment_method_list': paymentmethod_list,
            'menu_name':'Manual Delete Data'
        }
    )
    
def driving_guidelines(request):
   
    userlist = UserRecords.objects.all().order_by('lastname') 
   
    if request.user.is_authenticated:
        username = request.user
        user_id = username.id
        
        try:
            user_list = UserRecords.objects.get(authentication_user_id = user_id)
            fullname = user_list.firstname +' '+user_list.lastname  
        except:
            user_list = ''
            fullname = ''
            
    else:
        return redirect('/')
     
     
    return render(
        request,
        'admin_page/driving_guidelines.html',
        {
            'website_name': website_name,
            'userlist': userlist,
            'username': username,
            'fullname': fullname,
            'menu_name':'Driving Guidelines'
        }
    )

def website_images(request):
   
    userlist = UserRecords.objects.all().order_by('lastname') 
    system_settings_list = SystemSettings.objects.all().order_by('system_name')
    
    if request.user.is_authenticated:
        username = request.user
        user_id = username.id
        
        try:
            user_list = UserRecords.objects.get(authentication_user_id = user_id)
            fullname = user_list.firstname +' '+user_list.lastname  
        except:
            user_list = ''
            fullname = ''
     
    else:
        return redirect('/')
     
     
    return render(
        request,
        'admin_page/website_images.html',
        {
            'website_name': website_name,
            'userlist': userlist,
            'username': username,
            'fullname':fullname,
            'system_settings_list': system_settings_list,
            'menu_name':'Website Images'
        }
    )
    
    
def system_settings(request):
   
    userlist = UserRecords.objects.all().order_by('lastname') 
    
    
    form_system_settings = SystemSettingsForm()
    
    dt_now = datetime.datetime.now(tz=pytz.UTC)
    datetime_now = dt_now.astimezone(pytz.timezone('Asia/Manila'))
    dt_now = datetime.datetime.now()
   
    if request.user.is_authenticated:
    
        username = request.user
        user_id = username.id
        
        try:
            user_list = UserRecords.objects.get(authentication_user_id = user_id)
            fullname = user_list.firstname +' '+user_list.lastname  
        except:
            user_list = ''
            fullname = ''
            
    else:
        return redirect('/')
    
    if request.method == "POST":
    
        form_system_settings = SystemSettingsForm(request.POST or None)
        if(form_system_settings.is_valid()):
        
            SystemSettingsForm(request.POST)
            form_system_settings.cleaned_data
            form_system_settings.save()
            system_settings_list = SystemSettings.objects.all().order_by('id')           
     
        
    system_settings_list = SystemSettings.objects.all().order_by('id')
        
    return render(
        request,
        'admin_page/system_settings.html',
        {
            'website_name': website_name,
            'userlist': userlist,
            'system_settings_form':form_system_settings,
            'username': username,
            'fullname': fullname,           
            'datetime_now': dt_now,
            'system_settings_list': system_settings_list,
            'menu_name':'System Settings'
        }
    )
    
def system_settings_update(request):

    if request.method == "POST":
    
        system_settings_id                  = request.POST.get('system_settings_id',1)
        system_value_input                  = request.POST.get('system_value','--')
        system_name_input                   = request.POST.get('system_name','--')
        system_label_input                  = request.POST.get('system_label','--')
    
        system_setting_details              = SystemSettings.objects.get(id = system_settings_id)
        system_setting_details.system_label = system_label_input
        system_setting_details.system_name  = system_name_input
        system_setting_details.system_value = system_value_input
        system_setting_details.save()
    
        return redirect('system_settings')
    
def profile_view_admin(request):

    if request.user.is_authenticated:
    
        username = request.user
        user_id = username.id
        
        try:
            user_list               = UserRecords.objects.get(authentication_user_id = user_id)
            fullname                = user_list.firstname +' '+user_list.lastname  
            email_address           = user_list.email_address
            complete_address        = user_list.complete_address
            contact_number          = user_list.contact_number
        except:
            user_list = ''
            fullname = ''
            email_address = ''
            complete_address = ''
            contact_number = ''
        
    else:
        return redirect('/')  
     
    return render(    
         request,
        'admin_page/profile_view.html',       
        {
            'website_name': website_name,
            'username': username,
            'fullname': fullname,
            'email_address': email_address,
            'complete_address': complete_address,
            'contact_number': contact_number,
            'menu_name': 'Profile'
        }
    )

def notifications_admin(request):

    if request.user.is_authenticated:
    
        username = request.user
        user_id = username.id
        
        try:
            user_list               = UserRecords.objects.get(authentication_user_id = user_id)
            fullname                = user_list.firstname +' '+user_list.lastname  
            email_address           = user_list.email_address
            complete_address        = user_list.complete_address
            contact_number          = user_list.contact_number
        except:
            user_list = ''
            fullname = ''
            email_address = ''
            complete_address = ''
            contact_number = ''
        
    else:
        return redirect('/')  
     
    return render(    
         request,
        'admin_page/notifications.html',       
        {
            'website_name': website_name,
            'username': username,
            'fullname': fullname,
            'email_address': email_address,
            'complete_address': complete_address,
            'contact_number': contact_number,
            'menu_name': 'Profile'
        }
    )

def messages_admin(request):

    if request.user.is_authenticated:
    
        username = request.user
        user_id = username.id
        
        try:
            user_list               = UserRecords.objects.get(authentication_user_id = user_id)
            fullname                = user_list.firstname +' '+user_list.lastname  
            email_address           = user_list.email_address
            complete_address        = user_list.complete_address
            contact_number          = user_list.contact_number
        except:
            user_list = ''
            fullname = ''
            email_address = ''
            complete_address = ''
            contact_number = ''
        
    else:
        return redirect('/')  
     
    return render(    
         request,
        'admin_page/messages.html',       
        {
            'website_name': website_name,
            'username': username,
            'fullname': fullname,
            'email_address': email_address,
            'complete_address': complete_address,
            'contact_number': contact_number,
            'menu_name': 'Profile'
        }
    )
    
def activity_log_admin(request):

    if request.user.is_authenticated:
    
        username = request.user
        user_id = username.id
        
        try:
            user_list               = UserRecords.objects.get(authentication_user_id = user_id)
            fullname                = user_list.firstname +' '+user_list.lastname  
            email_address           = user_list.email_address
            complete_address        = user_list.complete_address
            contact_number          = user_list.contact_number
        except:
            user_list = ''
            fullname = ''
            email_address = ''
            complete_address = ''
            contact_number = ''
        
    else:
        return redirect('/')  
     
    return render(    
         request,
        'admin_page/activity_log.html',       
        {
            'website_name': website_name,
            'username': username,
            'fullname': fullname,
            'email_address': email_address,
            'complete_address': complete_address,
            'contact_number': contact_number,
            'menu_name': 'Profile'
        }
    )
    
def profile_logout_admin(request):
     logout_form(request)
     return redirect('/admin_page')
    
def home(request):
    
    userlist = UserRecords.objects.all().order_by('lastname') 
    system_settings_list = SystemSettings.objects.all().order_by('system_name')
      
    return render(
        request,
        'admin_page/login.html',
        {
            'website_name': website_name,
            'userlist': userlist,
            'system_settings_list': system_settings_list,
            'menu_name':'Login'
        }
    )
    
