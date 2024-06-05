from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    #date =
    stime = models.CharField(max_length=10)
    etime = models.CharField(max_length=10)
    name = models.CharField(max_length=10)
    add_to_checklist = models.BooleanField(default=False)
    done = models.BooleanField(default=False)
    class Meta:
        managed = False
        db_table = 'task'
