from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name = "home"),
    path('dashboard', views.dashboard, name = "dashboard"),
    path('payment', views.payment, name = "payment"),
    path('reference_no_update', views.reference_no_update, name = "reference_no_update"),
    path('transaction_details', views.transaction_details, name = "transaction_details"),
    path('logout_credentials', views.logout_credentials, name = "logout_credentials"),      
    path('skillsassessments', views.skillsassessments, name = "skillsassessments"),
    path('appointments', views.appointments, name = "appointments"),
    path('driving_guidelines', views.driving_guidelines, name = "driving_guidelines"),
    path('students', views.students, name = "students"),
    path('profile_view', views.profile_view, name = "profile_view"),
]