from django.db import models


class Grid(models.Model):
    time = models.IntegerField()
    minute = models.IntegerField()
    coloured = models.IntegerField()
    task = models.ForeignKey('Task', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'grid'
        unique_together = (('time', 'minute'),)


class Task(models.Model):
    stime = models.IntegerField(blank=True, null=True)
    etime = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    done = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'task'
