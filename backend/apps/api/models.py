from django.db import models
from django.contrib.auth.models import User

class SecureDropUser(models.Model):
    name   = models.CharField(max_length=180)
    email  = models.CharField(max_length=180, unique=True)
    passwd = models.CharField(max_length=180)

    pubkey = models.CharField(max_length=360)

    def __str__(self):
        return self.email

    class Meta:
        app_label = "api"