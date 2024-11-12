from django.db import models
from django.utils import timezone
from accounts.models import User

JOB_TYPE = (
    (1, "Full time"),
    (2, "Part time"),
    (3, "Internship"),
)

class Job(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    description = models.TextField()
    location = models.CharField(max_length=150)
    type = models.IntegerField(choices=JOB_TYPE)
    category = models.CharField(max_length=100)
    last_date = models.DateTimeField()
    company_name = models.CharField(max_length=100)
    company_description = models.CharField(max_length=300)
    website = models.CharField(max_length=100, default="")
    created_at = models.DateTimeField(default=timezone.now)
    filled = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.last_date < timezone.now():
            raise ValueError("Last date must be in the future.")
        super().save(*args, **kwargs)

    def __str__(self):
        return str(f"{self.title} at {self.company_name}")

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Job'
        verbose_name_plural = 'Jobs'


class Applicant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applicants')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.user.get_full_name())
