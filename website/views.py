from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core import serializers
from .models import UserRecords
from admin_page.models import SystemSettings, Course, Category, CategoryType, CarType, Enrolment
from .forms import SigninForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as login_form, logout as logout_form
from django.core.mail import send_mail, EmailMessage
from cruiser_driving import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from .tokens import generate_token
import json

# Create your views here.

website_name                    = 'Cruiser Driving School'
tagline                         = 'The Best Driving School with 10 Years of Excellence, Producing Skilled and Disciplined Driver'
address                         = 'Nueva Ecija'
contact                         = '09101111111'
company_email_address           = 'cruiser.driving2021@gmail.com'

category_list = Category.objects.all()
course_list = Course.objects.all()

def home_page(request):
    

    return render(
        request,
        'website/index.html',
        {
            'website_name': website_name,
            'menu_name':'Home',
            'categorylist':category_list,
            'tagline': tagline,
            'price_one': 20000
        }
    )

def about_us(request):
    return render(
        request,
        'website/about_us.html',
        {
            'categorylist':category_list,
            'courselist':course_list,
            'website_name': website_name,
            'menu_name':'About Us'
        }
    )
    
def contact(request):

   try:
       sys_info_map_link                     = SystemSettings.objects.get(system_name = "google_map_link")
       sys_info_company_address              = SystemSettings.objects.get(system_name = "company_address")
       sys_info_company_email_address        = SystemSettings.objects.get(system_name = "company_email_address")
       sys_info_company_phone_number         = SystemSettings.objects.get(system_name = "company_phone_number")
       sys_info_company_facebook_link        = SystemSettings.objects.get(system_name = "company_facebook_link")
       
       google_map_src                        = sys_info_map_link.system_value
       company_address                       = sys_info_company_address.system_value
       company_email_address                 = sys_info_company_email_address.system_value
       company_phone_number                  = sys_info_company_phone_number.system_value
       company_facebook_link                 = sys_info_company_facebook_link.system_value
       
   except:
   
       google_map_src                        = ''
       company_address                       = ''
       company_email_address                 = ''
       company_phone_number                  = ''
       company_facebook_link                 = ''
     
   return render(
        request,
        'website/contact.html',
        {
            'categorylist':category_list,
            'website_name': website_name,
            'google_map_link': google_map_src,
            'company_address': company_address,
            'company_phone_number': company_phone_number,
            'company_email_address': company_email_address,
            'company_facebook_link': company_facebook_link,
            'menu_name':'Contact Us'
        }
    )

def course_basic(request):
    
    name = 'Basic'

    return render(
        request,
        'website/courses.html',
        {
            'categorylist':category_list,
            'website_name': website_name,
            'menu_name':'Courses Offered',
            'course_difficulty': name
        }
    )
    
def course_intermediate(request):
    
    name = 'Intermediate'

    return render(
        request,
        'website/courses.html',
        {
            'categorylist':category_list,
            'website_name': website_name,
            'menu_name':'Courses Offered',
            'course_difficulty': name
        }
    )

def course_advanced(request):
    
    name = 'Advanced'
    context = {
        'categorylist':category_list,
        'website_name': website_name,
        'menu_name':'Courses Offered',
        'course_difficulty': name
    }
    
   
    return render(request,'website/courses.html',context)


    
def register(request):

    course_list = Course.objects.all()
    category_list = Category.objects.all()
    category_type_list = CategoryType.objects.all()
    car_type_list = CarType.objects.all()

    return render(
        request,
        'website/register.html',
        {
            'website_name': website_name,
            'menu_name':'Register',
            'category_list':category_list,
            'categorylist':category_list,
            'category_type_list':category_type_list,
            'car_type_list':car_type_list,
            'course_list':course_list
        }
    )

def register_process(request):
     
    course_list                 = Course.objects.all()
    
    username_input              = request.POST['username']   
    desired_password            = request.POST['desired_password']
    retry_password              = request.POST['retry_password']
    
    firstname_input             = request.POST['firstname']
    lastname_input              = request.POST['lastname']
    middlename_input            = request.POST['middlename']
    name_extension_input        = request.POST['name_extension'] 
    birthdate_input             = request.POST['birthdate'] 
    complete_address_input      = request.POST['complete_address'] 
    email_address_input         = request.POST['email_address'] 
    contact_number_input        = request.POST['contact_number'] 
    gender_input                = request.POST['gender'] 
    civil_status_input          = request.POST['civil_status']
    
    license_type_input          = request.POST['license_type']
    
    course_selected             = request.POST['preferred_course']
    payment_method_input        = request.POST['payment_method']
    payment_term_input          = request.POST['payment_term']
    amount_input                = request.POST['tuition_fee']
    
    ise_email_address = len(User.objects.filter(email = email_address_input))
    ise_contact_number = len(UserRecords.objects.filter(contact_number = contact_number_input))
    
    ise_username = len(User.objects.filter(username = username_input))
     
    # test if entered desired password and retry password matches 
    if desired_password != retry_password:
        messages.error(request, "Password did not match, Try Again")
        return redirect('register')
    else:
    
        # test if email address already exist in the database website_userrecords
        # UserRecords.objects.get function will not return empty row that's why try and except is used        
        
        if ise_email_address > 0:
            
            messages.error(request, "Email Address is already used by another user")
            return redirect('register')
            
        else:
        
            if ise_username > 0:            
               
                messages.error(request,"Username is already used by another user")
                return redirect('register')
                
            else:
        
                if ise_contact_number > 0:
                
                    messages.error(request,"Contact Number is already used by another user")
                    return redirect('register')
                
                else:
                
                    # after validation, data will be saved on different tables
                    
                    # data will be inserted to auth_user table using User class from models.py of the current app (admin_page)
                    
                    user_records = User.objects.create_user(username = username_input, email = email_address_input, password = desired_password, first_name = firstname_input, last_name = lastname_input, is_active = True)
                    user_records.save()
                    
                    # getting the id value from default User table of django-admin by specifying the email_address
                     
                    user_records_filter = User.objects.get(email = email_address_input)
                    inserted_id = user_records_filter.id
                    
                    # data will be inserted to website_userrecords by using UserRecords class from models.py of the current app
                    # authentation_user_id saves the value of id (foreign key) from auth_user
                    
                    user_information = UserRecords(
                        authentication_user_id      = inserted_id,
                        firstname                   = firstname_input,
                        lastname                    = lastname_input,
                        middlename                  = middlename_input,
                        name_extension              = name_extension_input,
                        birthdate                   = birthdate_input,       
                        complete_address            = complete_address_input,
                        email_address               = email_address_input,
                        contact_number              = contact_number_input,
                        gender                      = gender_input,
                        role_id                     = 1,
                        civil_status                = civil_status_input
                    )
                    
                    user_information.save()
                    
                    # data will be saved to transaction table using Transaction class in models.py of the current app
                    
                    user_enrolment = Enrolment(
                        user_id = inserted_id,
                        license_type = license_type_input,
                        enrolled_course = course_selected,
                        payment_method = payment_method_input,
                        payment_term = payment_term_input,
                        amount = amount_input,
                        status = "0"
                    )
                    
                    user_enrolment.save()
                    
                    # sending email address to applicant
                    # fail_silently = True bypasses unneccesary errors that might be encountered during the process
                    
                    subject = "Welcome to Cruiser Driving!"
                    message = "Hello "+ firstname_input +" "+ lastname_input +"! /n Please Click the Confirmation Link to activate your account!";
                    from_email = settings.EMAIL_HOST_USER
                    to_email = [user_records.email]
                    send_mail(subject, message, from_email, to_email, fail_silently = True)
                    
                    # sending another email message to applicant, this time with the comfirmation link to activate the registered account
                    # domain is the main URL of the whole project, e.g. in a localhost, 127.0.0.1:8000 
                    
                    current_site = get_current_site(request)
                    email_subject=  "Email Confirmation for User Login - Cruiser Driving School"
                    second_message = render_to_string('confirmation_message_email.html',{
                        'name': user_records.username,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user_records.pk)),
                        'token': generate_token.make_token(user_records),
                    })
                    
                    email = EmailMessage(
                        email_subject,
                        second_message,
                        settings.EMAIL_HOST_USER,
                        [user_records.email],
                    )
                    
                    email.fail_silently = True
                    email.send()
                    
                    # concatenate first_name, middle_name, last_name and name_extension of applicant and store it into fullname variable
                    
                    fullname = user_records.first_name + ' ' + middlename_input + ' ' + user_records.last_name + ' ' + name_extension_input
                    
                    # render the registration_complete.html page to display the information, preferred course and payment method and term entered by applicant
                    
                    return render(
                        request,
                        'website/registration_complete.html',
                        {
                            'website_name': website_name,
                            'menu_name':'Register',
                            'fullname': fullname,
                            'username':username_input,
                            'complete_address': complete_address_input,
                            'registered_email_address': email_address_input,
                            'registered_contact_number': contact_number_input,
                            'course_list':course_list,
                            'categorylist':category_list
                        }
                    )

# comfirmation link from the email address sent to applicant
    
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user_records = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user_records = None
        
    if user_records is not None and generate_token.check_token(user_records, token):
        user_records.is_active = True
        user_records.save()
        login_form(request, user_records)  
        return redirect('student_page/dashboard')
    else:
        return redirect('')
        
        
def sample_registration_view(request):

    course_list                 = Course.objects.all()
    
    username_input              = request.POST['username']   
    desired_password            = request.POST['desired_password']
    retry_password              = request.POST['retry_password']
    
    firstname_input             = request.POST['firstname']
    lastname_input              = request.POST['lastname']
    middlename_input            = request.POST['middlename']
    name_extension_input        = request.POST['name_extension'] 
    birthdate_input             = request.POST['birthdate'] 
    complete_address_input      = request.POST['complete_address'] 
    email_address_input         = request.POST['email_address'] 
    contact_number_input        = request.POST['contact_number'] 
    gender_input                = request.POST['gender'] 
    civil_status_input          = request.POST['civil_status']
    
    course_selected             = request.POST['preferred_course']
    payment_method_input        = request.POST['payment_method']
    payment_term_input          = request.POST['payment_term']
    amount_input                = request.POST['tuition_fee']
    
    ise_email_address = len(User.objects.filter(email = email_address_input))
    ise_contact_number = len(UserRecords.objects.filter(contact_number = contact_number_input))
    
    ise_username = len(User.objects.filter(username = username_input))
     
    # test if entered desired password and retry password matches 
    if desired_password != retry_password:
        messages.error(request, "Password did not match, Try Again")
        return redirect('register')
    else:
    
        # test if email address already exist in the database website_userrecords
        # UserRecords.objects.get function will not return empty row that's why try and except is used        
        
        if ise_email_address > 0:
            
            messages.error(request, "Email Address is already used by another user")
            return redirect('register')
            
        else:
        
            if ise_username > 0:            
               
                messages.error(request,"Username is already used by another user")
                return redirect('register')
                
            else:
        
                if ise_contact_number > 0:
                
                    messages.error(request,"Contact Number is already used by another user")
                    return redirect('register')
                
                else:
                
                    # after validation, data will be saved on different tables
                    
                    # data will be inserted to auth_user table using User class from models.py of the current app (admin_page)
                    
                    # user_records = User.objects.create_user(username = username_input, email = email_address_input, password = desired_password, first_name = firstname_input, last_name = lastname_input, is_active = True)
                    
                    
                    # getting the id value from default User table of django-admin by specifying the email_address                     
                 
                    inserted_id = 1
                    
                    # data will be inserted to website_userrecords by using UserRecords class from models.py of the current app
                    # authentation_user_id saves the value of id (foreign key) from auth_user
                    
                    user_information = UserRecords(
                        authentication_user_id      = inserted_id,
                        firstname                   = firstname_input,
                        lastname                    = lastname_input,
                        middlename                  = middlename_input,
                        name_extension              = name_extension_input,
                        birthdate                   = birthdate_input,       
                        complete_address            = complete_address_input,
                        email_address               = email_address_input,
                        contact_number              = contact_number_input,
                        gender                      = gender_input,
                        role_id                     = 1,
                        civil_status                = civil_status_input
                    )
                    
                   
                    
                    # data will be saved to transaction table using Transaction class in models.py of the current app
                    
                    user_enrolment = Enrolment(
                        user_id = inserted_id,
                        enrolled_course = course_selected,
                        payment_method = payment_method_input,
                        payment_term = payment_term_input,
                        amount = amount_input,
                        status = "0"
                    )                    
                 
                  
                    # concatenate first_name, middle_name, last_name and name_extension of applicant and store it into fullname variable
                    
                    fullname = firstname_input + ' ' + middlename_input + ' ' + lastname_input + ' ' + name_extension_input
                    
                    # render the registration_complete.html page to display the information, preferred course and payment method and term entered by applicant
                    
                    return render(
                        request,
                        'website/registration_complete.html',
                        {
                            'website_name': website_name,
                            'menu_name':'Register',
                            'fullname': fullname,
                            'username':username_input,
                            'complete_address': complete_address_input,
                            'registered_email_address': email_address_input,
                            'registered_contact_number': contact_number_input,
                            'course_list':course_list,
                            'categorylist':category_list
                        }
                    )

# comfirmation link from the email address sent to applicant
    
def login(request):

    # accessing the page for directly visiting the link
    
    if(request.method  == "GET"):    
        # form = SigninForm()        
        return render(request,'website/login.html',{'website_name': website_name,'menu_name':'Login'})    
    else:    
       
         # path from submittion login form using POST method
         
        if(request.method == "POST"):
        
            username_entered = request.POST['username']
            password_entered = request.POST['password']       
            
            # verifying if username and password are matched from auth_user database
            user = authenticate(username=username_entered,password = password_entered)
        
        # if record is not empty by executing the authentication
        
        if user is not None:
        
            # saving the session for accessing the student_page/dashboard            
            login_form(request, user)      
            
            # route to student_page/dashboard
            return redirect('student_page/dashboard')           
            
        else:      
            
            # displaying error message and rendering back to the login form page for student account            
            messages.error(request, "Credentials not found or invalid password")
            return render(request,'website/login.html',{'website_name': website_name,'menu_name':'Login'})

def error404(request, exception):
    data = {}
    return render(request, 'website/error404.html',data)
    
# XHR functions

def xhr_get_value(request):

    return_value = Category.get(id = category_id)
    
    response = {}
    response['category_list'] = serializers.serialize("json", return_value)
    return HttpResponse(response, content_type = "application/json")
    
def get_course_ids_from_category(request):

    category_id = request.GET['category_id']   
    
    return HttpResponse(category_id)
   
 