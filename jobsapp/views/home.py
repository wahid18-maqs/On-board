from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView

from jobsapp.forms import ApplyJobForm
from jobsapp.models import Job, Applicant


class HomeView(ListView):
    model = Job
    template_name = 'home.html'
    context_object_name = 'jobs'

    def get_queryset(self):
        return Job.objects.filter(filled=False)[:6]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['trendings'] = Job.objects.filter(created_at__month=timezone.now().month)[:3]
        return context


class SearchView(ListView):
    model = Job
    template_name = 'jobs/search.html'
    context_object_name = 'jobs'

    def get_queryset(self):
        location = self.request.GET.get('location')
        profession = self.request.GET.get('profession')
        return Job.objects.filter(location__icontains=location, title__icontains=profession)


class JobListView(ListView):
    model = Job
    template_name = 'jobs/jobs.html'
    context_object_name = 'jobs'
    paginate_by = 5


class JobDetailsView(DetailView):
    model = Job
    template_name = 'jobs/details.html'
    context_object_name = 'job'
    pk_url_kwarg = 'id'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj is None:
            raise Http404("Job doesn't exist")
        return obj


class ApplyJobView(CreateView):
    model = Applicant
    form_class = ApplyJobForm
    slug_field = 'job_id'
    slug_url_kwarg = 'job_id'

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            messages.info(request, 'Successfully applied for the job!')
            return self.form_valid(form)
        return HttpResponseRedirect(reverse_lazy('jobs:home'))

    def get_success_url(self):
        return reverse_lazy('jobs:jobs-detail', kwargs={'id': self.kwargs['job_id']})

    def form_valid(self, form):
        # Check if user already applied for the job
        if Applicant.objects.filter(user_id=self.request.user.id, job_id=self.kwargs['job_id']).exists():
            messages.info(self.request, 'You already applied for this job')
            return HttpResponseRedirect(self.get_success_url())

        # Save new applicant
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)
