from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView, ListView

from accounts.forms import EmployeeProfileUpdateForm
from accounts.models import User
from jobsapp.models import Job, Applicant
from jobsapp.decorators import user_is_employee


class List_Application(ListView):
    model = Job
    template_name = 'accounts/employee/application.html'
    context_object_name = 'jobs'

    def get_queryset(self):
        id_set = User.objects.values('id').filter(email = self.request.user)
        job_set = Applicant.objects.filter(user_id__in = id_set.values_list('id')).values('job_id')
        return self.model.objects.filter(id__in = job_set.values_list('job_id'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class EditProfileView(UpdateView):
    model = User
    form_class = EmployeeProfileUpdateForm
    context_object_name = 'employee'
    template_name = 'jobs/employee/edit-profile.html'
    success_url = reverse_lazy('jobs:home')

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    @method_decorator(user_is_employee)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            raise Http404("User doesn't exists")
        # context = self.get_context_data(object=self.object)
        return self.render_to_response(self.get_context_data())

    def get_object(self, queryset=None):
        obj = self.request.user
        print(obj)
        if obj is None:
            raise Http404("Job doesn't exists")
        return obj
