from django.views import generic
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse_lazy
from .models import Task
from .forms import UserForm, LoginUserForm, TaskSearchingForm
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin

class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'tasks/index.html'
    context_object_name = "all_tasks"

    def get_queryset(self):
        user = self.request.user.id
        tasks = Task.objects.filter(user_id=user)
        return tasks

class DetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    template_name = 'tasks/detail.html'

class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'task_image']

    def form_valid(self, form):
        task = form.save(commit=False)
        user = self.request.user
        task.user_id = user
        task.save()
        return super(TaskCreate, self).form_valid(form)

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'task_image']

class TaskDelete(LoginRequiredMixin, DeleteView):
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

class LoginView(View):
    form_class = LoginUserForm
    template_name = 'tasks/login.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect("tasks:index")
            else:
                return redirect("Inactive user.")
        else:
            return redirect("tasks:index")

        return render(request, self.template_name, {'form': form})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("tasks:login")

class SearchList(LoginRequiredMixin, generic.ListView):
    model = Task
    form_class = TaskSearchingForm
    template_name = 'tasks/search.html'
    context_object_name = 'search_results'

    def get_queryset(self):
        search = self.request.GET.get("q")
        if search:
            queryset = Task.objects.filter(Q(title__icontains=search)).distinct
            return queryset