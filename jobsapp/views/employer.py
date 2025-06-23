from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, FileResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView
from reportlab.pdfgen import canvas

from jobsapp.decorators import user_is_employer
from jobsapp.forms import CreateJobForm
from jobsapp.models import Job, Applicant
from accounts.models import User


class BaseEmployerView:
    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    @method_decorator(user_is_employer)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class DashboardView(BaseEmployerView, ListView):
    model = Job
    template_name = 'jobs/employer/dashboard.html'
    context_object_name = 'jobs'

    def get_queryset(self):
        return Job.objects.filter(user_id=self.request.user.id)


class ApplicantPerJobView(BaseEmployerView, ListView):
    model = Applicant
    template_name = 'jobs/employer/applicants.html'
    context_object_name = 'applicants'
    paginate_by = 5

    def get_queryset(self):
        return Applicant.objects.filter(job_id=self.kwargs['job_id']).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['job'] = Job.objects.get(id=self.kwargs['job_id'])
        return context


class JobCreateView(BaseEmployerView, CreateView):
    model = Job  
    form_class = CreateJobForm
    template_name = 'jobs/create.html'
    extra_context = {'title': 'Post New Job'}
    success_url = reverse_lazy('jobs:employer-dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ApplicantsListView(BaseEmployerView, ListView):
    model = Applicant
    template_name = 'jobs/employer/all-applicants.html'
    context_object_name = 'applicants'

    def get_queryset(self):
        return Applicant.objects.filter(job__user_id=self.request.user.id)


@login_required(login_url=reverse_lazy('accounts:login'))
def filled(request, job_id=None):
    Job.objects.filter(user_id=request.user.id, id=job_id).update(filled=True)
    return HttpResponseRedirect(reverse_lazy('jobs:employer-dashboard'))


@login_required(login_url=reverse_lazy('accounts:login'))
def delete_job(request, job_id=None):
    Job.objects.filter(user_id=request.user.id, id=job_id).delete()
    return HttpResponseRedirect(reverse_lazy('jobs:employer-dashboard'))


@login_required(login_url=reverse_lazy('accounts:login'))
def download_resume(request, user_id):
    uploaded_file = User.objects.get(id=user_id)
    response = HttpResponse(uploaded_file.resume)
    response['Content-Disposition'] = f'attachment; filename="{uploaded_file.resume.name[7:]}"'
    return response


@login_required(login_url=reverse_lazy('accounts:login'))
def pdf_applicants(request, user_id):
    from io import BytesIO
    buffer = BytesIO()
    p = canvas.Canvas(buffer)

    applications = Applicant.objects.filter(job__user_id=user_id)
    company_name = User.objects.get(id=user_id).first_name
    p.drawString(100, 750, f"Application for Job posted by {company_name}")

    y = 700
    for row in applications:
        name = f"{row.user.first_name} {row.user.last_name}"
        p.drawString(100, y, f"Name: {name}")
        p.drawString(100, y - 20, f"Job title: {row.job.title}")
        p.drawString(100, y - 40, f"Email: {row.user.email}")
        p.drawString(100, y - 60, f"Date: {row.created_at}")
        y -= 100

    p.showPage()
    p.save()

    #pdf generate
    buffer.seek(0)
    filename = f"{company_name}.pdf"
    return FileResponse(buffer, as_attachment=True, filename=filename)
