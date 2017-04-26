from django.http import Http404
from django.shortcuts import render
from .models import Task

# Create your views here.
def index(request):
    all_tasks = Task.objects.all()
    return render(request, "tasks/index.html", {'all_tasks' : all_tasks})

def detail(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        raise Http404("Task Does Not Exist")
    return render(request, "tasks/detail.html", {'task' : task})