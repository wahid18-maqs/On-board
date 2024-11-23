from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView, ListView

from accounts.forms import EmployeeProfileUpdateForm
from accounts.models import User
from jobsapp.models import Job, Applicant
from jobsapp.decorators import user_is_employee


class ListApplication(ListView):
    model = Job
    template_name = 'accounts/employee/application.html'
    context_object_name = 'jobs'

    def get_queryset(self):
        user_id = User.objects.get(email=self.request.user.email).id
        job_ids = Applicant.objects.filter(user_id=user_id).values_list('job_id', flat=True)
        return Job.objects.filter(id__in=job_ids)


class EditProfileView(UpdateView):
    model = User
    form_class = EmployeeProfileUpdateForm
    context_object_name = 'employee'
    template_name = 'jobs/employee/edit-profile.html'
    success_url = reverse_lazy('jobs:home')

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    @method_decorator(user_is_employee)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        try:
            return self.request.user
        except User.DoesNotExist:
            raise Http404("User does not exist")
