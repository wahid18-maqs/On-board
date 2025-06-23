from django.apps import AppConfig
from .keepalive import start_ping_thread  

class JobsappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'jobsapp'

    def ready(self):
        start_ping_thread()  
