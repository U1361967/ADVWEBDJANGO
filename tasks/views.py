from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from .models import Task

class IndexView(generic.ListView):
    template_name = 'tasks/index.html'
    context_object_name = "all_tasks"

    def get_queryset(self):
        return Task.objects.all()

class DetailView(generic.DetailView):
    model = Task
    template_name = 'tasks/detail.html'

class TaskCreate(CreateView):
    model = Task
    fields = ['title', 'description']

class TaskUpdate(UpdateView):
    model = Task
    fields = ['title', 'description']

class TaskDelete(DeleteView):
    model = Task
    success_url = reverse_lazy('tasks:index')