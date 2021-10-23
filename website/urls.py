from django.urls import path, reverse
from . import views

#website urls

urlpatterns = [

path('',views.home_page, name = 'home_page'),
path('about_us',views.about_us, name = 'about_us'),
path('course_basic',views.course_basic, name = 'course_basic'),
path('course_intermediate',views.course_intermediate, name = 'course_intermediate'),
path('course_advanced',views.course_advanced, name = 'course_advanced'),
path('contact',views.contact, name = 'contact'),
path('register',views.register, name = 'register'),
path('register_process',views.register_process, name = 'register_process'),
path('sample_registration_view',views.sample_registration_view, name = 'sample_registration_view'),
path('login',views.login, name = 'login'),
path('get_course_ids_from_category',views.get_course_ids_from_category, name = 'get_course_ids_from_category'),
path('activate/<uidb64>/<token>',views.activate, name = 'activate'),

 
]

