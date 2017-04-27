from django.views import generic
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse_lazy
from .models import Task
from .forms import UserForm

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

class UserFormView(View):
    form_class = UserForm
    template_name = 'tasks/registration_form.html'

    # Display A Blank Form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name,{'form': form})

    # Process Form Data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            #Cleaned/Normalised Data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            # Return User Object If Credentials Are Correct
            user = authenticate(username=username,password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('tasks:index')

        return render(request, self.template_name, {'form': form})
