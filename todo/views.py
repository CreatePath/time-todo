from django.shortcuts import render

# Create your views here.
from todo.models import Task
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Task
import json

def main(request):
    tasks = Task.objects.all()
    return render(request, 'todo/main.html', {'tasks': tasks})

@csrf_exempt
def create_task(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        task = Task(
            stime=data['stime'],
            etime=data['etime'],
            name=data['name'],
            add_to_checklist=data['add_to_checklist'],
            done=data.get('done', False),
        )
        task.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@csrf_exempt
def read_tasks(request):
    if request.method == 'GET':
        tasks = Task.objects.all().values('stime', 'etime', 'name', 'add_to_checklist')
        tasks_list = list(tasks)
        return JsonResponse(tasks_list, safe=False)
    else:
        return JsonResponse({'error': '잘못된 요청'}, status=400)

@csrf_exempt
def update_task(request, task_id):
    if request.method == 'PUT':
        data = json.loads(request.body)
        task = Task.objects.get(id=task_id)
        task.stime = data['stime']
        task.etime = data['etime']
        task.name = data['name']
        task.add_to_checklist = data['add_to_checklist']
        task.done = data.get('done', False),
        task.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)

@csrf_exempt
def delete_task(request, task_id):
    if request.method == 'DELETE':
        task = Task.objects.get(id=task_id)
        task.delete()
        return JsonResponse({'status': 'success'})