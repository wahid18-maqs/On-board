from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView

from jobsapp.decorators import user_is_employer
from jobsapp.forms import CreateJobForm
from jobsapp.models import Job, Applicant
from accounts.models import User
from django.http import FileResponse
from reportlab.pdfgen import canvas

class DashboardView(ListView):
    model = Job
    template_name = 'jobs/employer/dashboard.html'
    context_object_name = 'jobs'

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    @method_decorator(user_is_employer)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(user_id=self.request.user.id)


class ApplicantPerJobView(ListView):
    model = Applicant
    template_name = 'jobs/employer/applicants.html'
    context_object_name = 'applicants'
    paginate_by = 5

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    @method_decorator(user_is_employer)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        return Applicant.objects.filter(job_id=self.kwargs['job_id']).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['job'] = Job.objects.get(id=self.kwargs['job_id'])
        return context


class JobCreateView(CreateView):
    template_name = 'jobs/create.html'
    form_class = CreateJobForm
    extra_context = {
        'title': 'Post New Job'
    }
    success_url = reverse_lazy('jobs:employer-dashboard')

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    @method_decorator(user_is_employer)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user 
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response({'form': form})


class ApplicantsListView(ListView):
    model = Applicant
    template_name = 'jobs/employer/all-applicants.html'
    context_object_name = 'applicants'

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    def get_queryset(self):
        return self.model.objects.filter(job__user_id=self.request.user.id)


@login_required(login_url=reverse_lazy('accounts:login'))
def filled(request, job_id=None):
    job = Job.objects.get(user_id=request.user.id, id=job_id)
    job.filled = True
    job.save()
    return HttpResponseRedirect(reverse_lazy('jobs:employer-dashboard'))


@login_required(login_url=reverse_lazy('accounts:login'))
def delete_job(request, job_id=None):
    job = Job.objects.get(user_id=request.user.id, id=job_id)
    job.delete()
    return HttpResponseRedirect(reverse_lazy('jobs:employer-dashboard'))


@login_required(login_url=reverse_lazy('accounts:login'))
def download_resume(request, user_id):
    uploaded_file = User.objects.get(id=user_id)
    response = HttpResponse(uploaded_file.resume)
    file_name = str(uploaded_file.resume.name)
    response['Content-Disposition'] = f'attachment; filename="{file_name[7:]}"'
    return response


@login_required(login_url=reverse_lazy('accounts:login'))
def pdf_applicants(request, user_id):
    from io import BytesIO
    buffer = BytesIO()
    p = canvas.Canvas(buffer)

    applications = Applicant.objects.filter(job__user_id=user_id)

    company_name = User.objects.filter(id=user_id).values('first_name')
    company_name = company_name[0]
    p.drawString(100, 750, f"Application for Job posted by {company_name['first_name']}")

    y = 700
    for row in applications:
        name = row.user.first_name + " " + row.user.last_name
        p.drawString(100, y, f"Name: {name}")
        p.drawString(100, y - 20, f"Job title: {row.job.title}")
        p.drawString(100, y - 40, f"Email: {row.user.email}")
        p.drawString(100, y - 60, f"Date: {row.created_at}")
        y -= 100

    p.showPage()
    p.save()

    buffer.seek(0)
    filename = f"{company_name['first_name']}.pdf"
    return FileResponse(buffer, as_attachment=True, filename=filename)
