from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stime = models.IntegerField(blank=True, null=True)
    etime = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    done = models.IntegerField(blank=True, null=True)



class Grid(models.Model):
    time = models.IntegerField()
    minute = models.IntegerField()
    coloured = models.IntegerField()
    task = models.ForeignKey('Task', models.DO_NOTHING, blank=True, null=True)