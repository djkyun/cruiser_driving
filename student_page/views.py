from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from website.models import UserRecords
from admin_page.models import LoginHistory, Course, SystemSettings, Category, PaymentMethodList, Enrolment, SalesTransaction, Appointment, TimeScheduleAppointment, ScheduleType, Attendance, Rooms, Lesson, LessonDetailTitle, LessonDetail, InstructorSpecialization, CategoryType, CarType
from website.models import UserRecords
from django.contrib.auth.models import User as UserCredential
from django.contrib.auth import login as login_form, logout as logout_form
from django.contrib import messages
import datetime, math

# Create your views here.

url_base = '127.0.0.1:8000/'
website_name = 'Cruiser Driving School'

def dashboard(request):
   
    userlist = ''
    
    if request.user.is_authenticated:
        username = request.user
        user_id = username.id
       
        user_list               = UserRecords.objects.get(authentication_user_id = user_id)
        fullname                = user_list.firstname +' '+user_list.lastname
        role_id                 = user_list.role_id
        gender                  = user_list.gender
        birthdate               = user_list.birthdate
        email_address           = user_list.email_address
        contact_number          = user_list.contact_number
        complete_address        = user_list.complete_address
        civil_status            = user_list.civil_status
        
       

        payment_method_list     = PaymentMethodList.objects.all()
        
        enrolment_record        = Enrolment.objects.get(user_id = user_id)
        course_id               = enrolment_record.enrolled_course
        payment_term            = enrolment_record.payment_term
        payment_method          = enrolment_record.payment_method
        amount                  = enrolment_record.amount
        enrolment_id            = enrolment_record.id
        
        if len(payment_method_list) == 2:
            payment_term = 2
        
        course_list             = Course.objects.get(id = course_id)
        course_name             = course_list.course_name
        category_id             = course_list.category_id
        
        category_list           = Category.objects.get(id = category_id)
        category_name           = category_list.category_name
        
        system_settings         = SystemSettings.objects.get(system_name = 'gcash_number')
        payment_phone           = system_settings.system_value
        
        system_settings         = SystemSettings.objects.get(system_name = 'company_address')
        payment_address         = system_settings.system_value
        
        partial_payment         = float(amount) * .50
        
      
        
        sales_transaction_count = 0
        
        try:
        
            sales_transaction   = SalesTransaction.objects.filter(enrolment_id = enrolment_id)       
            sales_transaction_count = len(SalesTransaction.objects.filter(enrolment_id = enrolment_id))
            
        except:
            
            sales_transaction   = '--'
        
      
        age                     = get_age(birthdate)    
        bdate                   = convert_readable_date(birthdate)
        
     
    else:
        return redirect('/')
   
    return render(   
       request,   
       'student_page/index.html',
       {
            'website_name': website_name,
            'menu_name':'Home',
            'username': username,           
            'fullname': fullname,           
            'gender': gender,           
            'birthdate': bdate,           
            'age': age,           
            'civil_status': get_civil_status(civil_status),           
            'contact_number': contact_number,           
            'complete_address': complete_address,           
            'email_address': email_address,           
            'category_name': category_name,           
            'course_name': course_name,           
            'enrolment_id': enrolment_id,           
            'payment_method': payment_method,           
            'partial_payment': partial_payment,           
            'payment_term': payment_term,         
            'payment_phone': payment_phone,           
            'payment_address': payment_address,       
            'amount': amount,            
            'sales_transaction_list': sales_transaction,  
            'sales_transaction_count':sales_transaction_count,
            'payment_method_list': payment_method_list,           
            'userlist': userlist,
            'url_base': url_base,
            'role_id': role_id,
            'user_id': user_id,
            'user_credentials': UserCredential
           
       }   
   )
   
def is_fully_paid(status, for_payment_term):
    
    stat = 0
    
    # fully paid = 1
    # not fully paid = 0
    
    if status == '1':
        if for_payment_term == '2':
            stat = 1
        if for_payment_term == '1':
            stat = 0
    else:
        stat = 0
    
    return stat
   
def get_civil_status(cs):

    value_var = ''
    
    if cs == '1':
        value_var = "Single"
    if cs == '2':
        value_var = "Married"
    if cs == '3':
        value_var = "Separated"
        
    return value_var
    
def get_age(birthdate):

    array_bdate             = birthdate.split('-')
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
    
def convert_readable_date(date_here):

    array_date             = date_here.split('-')
    year                   = int(array_date[0])
    month                  = int(array_date[1])
    day                    = int(array_date[2])

    date_return            = datetime.date(year, month, day)
    
    return date_return
    
            
def transaction_details(request):

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
        
    a_user_id               = user_list.authentication_user_id    
    sales_transaction_list  = SalesTransaction.objects.filter(user_id = a_user_id);
    course_list             = Course.objects.all();
    enrolment_list          = Enrolment.objects.all();
    payment_method_list     = PaymentMethodList.objects.all();   

    return render(
        request,
        'student_page/transaction_details.html',
        {
            'username': username,
            'fullname': fullname,
            'menu_name':'Transaction Details',
            'sales_transaction_list':sales_transaction_list,
            'payment_method_list':payment_method_list,            
            'course_list':course_list,
            'enrolment_list':enrolment_list
        }
    )
    
def payment(request):
    
    sales_transaction = SalesTransaction(
        user_id = request.POST['user_id'],
        enrolment_id = request.POST['enrolment_id'],
        user_contact_number = request.POST['contact_number'],
        payment_contact_number = request.POST['payment_phone'],
        payment_reference_no = request.POST['payment_reference_no'],
        for_payment_term = request.POST['for_payment_term'],
        payment_term = request.POST['payment_term'],
        payment_method = request.POST['payment_method_input'],
        transaction_type = 1
    )
    
    sales_transaction.save()
    
    messages.success(request, "Reference Number/Control Number Submitted!")
    
    return redirect('dashboard')
    
def reference_no_update(request):
    
    sales_transaction_id                    = request.POST['sales_transaction_id']
    sales_transaction                       = SalesTransaction.objects.get(id = sales_transaction_id)       
    
    sales_transaction.payment_reference_no  = request.POST['payment_reference_no']
    sales_transaction.save()
    
    messages.success(request, "Reference Number/Control Number Updated!")
    
    return redirect('dashboard')
    
def skillsassessments(request):

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
        'student_page/skills_assessments.html',
        {            
            'username': username,
            'fullname': fullname,
            'menu_name':'Skills Assessments'
        }
    )
 
def appointments(request):

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
    
    a_user_id               = user_list.authentication_user_id   
        
    course_list             = Course.objects.all()
    
    enrolment_list          = Enrolment.objects.get(user_id = a_user_id)
    enrolment_id_found      = enrolment_list.id
    
    attendance_list         = Attendance.objects.filter(enrolment_id = enrolment_id_found)
    timeschedule_list       = TimeScheduleAppointment.objects.all().order_by('id')
    appointment_list        = Appointment.objects.all().order_by('id')
    instructor_list         = UserRecords.objects.all()
    room_list               = Rooms.objects.all()

    return render(
        request,
        'student_page/appointments.html',
        {            
            'username':username,
            'fullname':fullname,
            'menu_name':'Appointments',
            'course_list':course_list,
            'attendance_list':attendance_list,
            'timeschedule_list':timeschedule_list,
            'appointment_list':appointment_list,
            'instructor_list':instructor_list,
            'room_list':room_list
        }
    )

def driving_guidelines(request):

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
        'student_page/driving_guidelines.html',
        {
            'username':username,
            'fullname':fullname,
            'menu_name':'Driving Guidelines'
        }
    )
    
def students(request):

    userlist = ''
      
    return render(
        request,
        'student_page/students.html',
        {
            'website_name': website_name,
            'userlist': userlist,
            'menu_name':'Students List'
        }
    )
    
def profile_view(request):

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
        'student_page/profile_view.html',       
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
    
def logout_credentials(request):
    logout_form(request)
    return redirect('/')
    
def home(request):
    
    return HttpResponse('Home Page')
