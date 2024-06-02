from django.shortcuts import render

# Create your views here.
from todo.models import Task, Grid
from django.shortcuts import render, redirect

def task_grid_view(request):
    tasks = Task.objects.all()
    grids = Grid.objects.all()
    return render(request, 'todo/task_grid.html', {'tasks': tasks, 'grids': grids})

def add_task(request):
    # 추가 기능 구현
    return render(request, 'add_task.html')

def edit_task(request, task_id):
    # 수정 기능 구현
    return render(request, 'edit_task.html', {'task_id': task_id})