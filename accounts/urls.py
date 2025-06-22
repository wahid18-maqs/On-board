from django.urls import path

# Import only once from correct locations
from jobsapp.views.employee import ListApplication,EditProfileView
from .views import RegisterEmployeeView, RegisterEmployerView, LogoutView, LoginView

app_name = "accounts"

urlpatterns = [
    path('employee/register', RegisterEmployeeView.as_view(), name='employee-register'),
    path('employer/register', RegisterEmployerView.as_view(), name='employer-register'),
    path('employee/application', ListApplication.as_view(), name='employee-application'),
    path('employee/profile/update', EditProfileView.as_view(), name='employee-profile-update'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('login', LoginView.as_view(), name='login'),
]
