from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from website.models import UserRecords
from django.contrib.auth import login as login_form, authenticate, logout as logout_form

# Create your views here.

url_base = '127.0.0.1:8000/'
website_name = 'Cruiser Driving School'

total_number_applicants = UserRecords.objects.all().count()
total_number_students = len(UserRecords.objects.all())
total_number_completed_students = len(UserRecords.objects.all())
average_number_students_per_course = len(UserRecords.objects.all())
average_age_students = len(UserRecords.objects.all())
enrolled_hours_ratio = len(UserRecords.objects.all())

def login_instructor(request):
    
    menu_name = 'Instructor Login'
    
    if(request.method == "POST"):
    
        username_input          = request.POST['username']
        password_input          = request.POST['password']
        
        user_credential_info    = authenticate(username = username_input, password = password_input)
        user_id                 = user_credential_info.id      
        
        user_list               = UserRecords.objects.get(authentication_user_id = user_id)
        fullname                = user_list.firstname +' '+user_list.lastname
        role_id                 = user_list.role_id
        
        userlist                = UserRecords.objects.all().order_by('id')
        
        
        if user_credential_info is not None:        
          
           if(str(role_id) == "3"):
            
               login_form(request, user_credential_info)      
               
               return render(
               
                   request,   
                   'instructor_page/index.html',
                       {
                            'website_name': website_name,
                            'menu_name':'Home',
                            'username': username_input,
                            'fullname': fullname,
                            'userlist': userlist,
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
           
                messages.error(request,"You cannot login account here!")
           
            
        else:
            
            messages.error(request,"User credential not found or invalid password")
             
            return render(
                request,
                'instructor_page/login.html',                
                {
                    'website_name':website_name,
                    'menu_name': menu_name
                }
            )
            
           
    
    else:
    
        return HttpResponse('request not allowed')
        
def dashboard(request):
    
   userlist = ''
   
   if request.user.is_authenticated:
        username = request.user
        user_id = username.id
        
        user_list = UserRecords.objects.get(authentication_user_id = user_id)
        fullname = user_list.firstname +' '+user_list.lastname
     
   else:
        return redirect('/')
   
   return render(
   
   request,   
   'instructor_page/index.html',
       {
            'website_name': website_name,
            'menu_name':'Home',
            'username': username,
            'fullname': fullname,
            'userlist': userlist,
            'url_base': url_base,
            'total_number_applicants': total_number_applicants
       }
   
   )
   
def add_user(request):

    return render(
        request,
        'instructor_page/add_user.html',
        {
            'menu_name':'Add User'
        }
    )
    

def students(request):

    userlist = ''
      
    return render(
        request,
        'instructor_page/students.html',
        {
            'website_name': website_name,
            'userlist': userlist,
            'menu_name':'Students List'
        }
    )
    
def profile_logout(request):
     logout_form(request)
     return redirect('/instructor_page')
    
    
def home(request):
    
    userlist = UserRecords.objects.all().order_by('lastname')     
      
    return render(
        request,
        'instructor_page/login.html',
        {
            'website_name': website_name,
            'userlist': userlist,           
            'menu_name':'Login'
        }
    )
