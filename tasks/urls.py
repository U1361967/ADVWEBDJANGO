from django.conf.urls import url
from . import views

app_name = 'tasks'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name="index"), # /tasks/
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name="detail"), #/tasks/[taskid]/
    url(r'tasks/add/$', views.TaskCreate.as_view(), name="create_task"), #/tasks/add/
    url(r'edit/(?P<pk>[0-9]+)/$', views.TaskUpdate.as_view(), name="update_task"),  # /tasks/2/
    url(r'tasks/(?P<pk>[0-9]+)/delete/$', views.TaskDelete.as_view(), name="delete_task"),  # /tasks/2/delete
    url(r'^register/$', views.UserFormView.as_view(), name="register"), # /register/
    url(r'^login/$', views.LoginView.as_view(), name="login"), # /login/
    url(r'^logout/$', views.LogoutView.as_view(), name="logout"), # /logout/

]
