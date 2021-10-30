from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name = "home"),
    path('login_instructor', views.login_instructor, name = "login_instructor"),
    path('skills_assessments_instructor', views.skills_assessments_instructor, name = "skills_assessments_instructor"),
    path('dashboard', views.dashboard, name = "dashboard"),
    path('add_user', views.add_user, name = "add_user"),
    path('create_user', views.add_user, name = "add_user"),
    path('students', views.students, name = "students"),
    path('profile_logout', views.profile_logout, name = "profile_logout"),   
]