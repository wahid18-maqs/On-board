from django.urls import path, include

from .views import *

app_name = "jobs"

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('search', SearchView.as_view(), name='search'),
    path('employer/dashboard', include([
        path('', DashboardView.as_view(), name='employer-dashboard'),
        path('all-applicants', ApplicantsListView.as_view(), name='employer-all-applicants'),
        path('applicants/<int:job_id>', ApplicantPerJobView.as_view(), name='employer-dashboard-applicants'),
        path('download-resume/<int:user_id>', download_resume, name='download-resume'),
        path('mark-filled/<int:job_id>', filled, name='job-mark-filled'),
        path('delete-job/<int:job_id>', delete_job, name='delete-job'),
        path('applicant-pdf/<int:user_id>', pdf_applicants, name="applicant-pdf")
        
    ])),
    path('apply-job/<int:job_id>', ApplyJobView.as_view(), name='apply-job'),
    path('jobs', JobListView.as_view(), name='jobs'),
    path('jobs/<int:id>', JobDetailsView.as_view(), name='jobs-detail'),
    path('employer/jobs/create', CreateView.as_view(), name='employer-jobs-create'),
    
]