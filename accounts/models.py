from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
import os
from accounts.managers import UserManager

GENDER_CHOICES = (
    ('male', 'Male'),
    ('female', 'Female'))


##for saving updated resume
def save_files(instance, filename):
    upload_to = 'resume/'
    ext = filename.split('.')[-1]

    if instance.id:
        filename = '{}_{}.{}'.format(instance.first_name, instance.id, ext)
        file_path = os.path.join(settings.MEDIA_ROOT, 'resume/')
        if os.path.exists(file_path+filename):
            os.remove(file_path+filename)
        
    return os.path.join(upload_to,filename)




class User(AbstractUser):
    username = None
    role = models.CharField(max_length=12, error_messages={'required': "Role to be provided"})
    gender = models.CharField(max_length=10, blank=True, null=True, default="")
    email = models.EmailField(unique=True, blank=False,
                              error_messages={
                                  'unique': "A user with that email already exists.",
                              })
    
    resume = models.FileField(upload_to=save_files)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __unicode__(self):
        return self.email

    objects = UserManager()
