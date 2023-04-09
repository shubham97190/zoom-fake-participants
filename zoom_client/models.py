from django.db import models

# Create your models here.

class StoreMetting(models.Model):
    meeting_code        = models.CharField(max_length=50)
    meeting_password    = models.CharField(max_length=50)
    no_of_participants  = models.PositiveSmallIntegerField(default=0)
