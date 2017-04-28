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

# This Class Will Show The View For The Task Index Page
class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'tasks/index.html'
    context_object_name = "all_tasks"

# This Class Queryset Grabs The Tasks Linked To The User
    def get_queryset(self):
        user = self.request.user.id
        tasks = Task.objects.filter(user_id=user)
        return tasks

# This Will Show The View For The Task Details Page
class DetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    template_name = 'tasks/detail.html'

# This Class Will Show The View To Create A Task With The Stated Fields
class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'task_image']

# This Class Shall Save The Task With The User's ID
    def form_valid(self, form):
        task = form.save(commit=False)
        user = self.request.user
        task.user_id = user
        task.save()
        return super(TaskCreate, self).form_valid(form)

# This Class Shall Show The Update Task With The Stated Fields
class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'task_image']

# This Class Shall Delete A Task
class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('tasks:index')

# This Class Shall Show The Registation Form
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

        # If The Form Input Contains Valid Information Save The Information
        if form.is_valid():
            user = form.save(commit=False)
            #Cleaned/Normalised Data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            # Return User Object If Credentials Are Correct
            user = authenticate(username=username,password=password)

            # If User Is Already Logged In
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('tasks:index')

        return render(request, self.template_name, {'form': form})

# This Class Shall Show The Login View
class LoginView(View):
    form_class = LoginUserForm
    template_name = 'tasks/login.html'

    # Get Method
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # Post Method
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        # If User Is Already Logged In
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect("tasks:index")
            else:
                return redirect("Inactive user.")
        else:
            return redirect("tasks:index")

# This Class Shall Log Out A User
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("tasks:login")

# This Class Shall Handle The Search Query And Also Show The Search Results View
class SearchList(LoginRequiredMixin, generic.ListView):
    model = Task
    form_class = TaskSearchingForm
    template_name = 'tasks/search.html'
    context_object_name = 'search_results'

    # This Queryset Shall Process The Search
    def get_queryset(self):
        search = self.request.GET.get("q")
        if search:
            queryset = Task.objects.filter(Q(title__icontains=search)).distinct
            return queryset