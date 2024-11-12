from django.urls import path, include


from jobsapp.views import EditProfileView, List_Application
from .views import *

app_name = "accounts"

urlpatterns = [
    path('employee/register', RegisterEmployeeView.as_view(), name='employee-register'),
    path('employer/register', RegisterEmployerView.as_view(), name='employer-register'),
    path('employee/application', List_Application.as_view(), name='employee-application'),
    path('employee/profile/update', EditProfileView.as_view(), name='employee-profile-update'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('login', LoginView.as_view(), name='login'),
]
