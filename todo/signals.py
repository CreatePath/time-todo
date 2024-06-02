from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.apps import apps
from todo.models import Task, Grid

@receiver(post_migrate)
def create_initial_data(sender, **kwargs):
    if sender.name == 'todo':
        #if not Task.objects.exists():
        #task11 = Task.objects.create(stime=800, etime=900, name='Task 11', done=False)
        if not Grid.objects.exists():
            for t in range(6,24):
                for m in range(0, 60, 10):
                    Grid.objects.create(time=t, minute=m, coloured=False, task=None)
