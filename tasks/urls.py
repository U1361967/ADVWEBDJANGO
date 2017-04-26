from django.conf.urls import url
from . import views

app_name = 'tasks'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name="index"), # /tasks/
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name="detail"), #/tasks/[taskid]/
    url(r'tasks/add/$', views.TaskCreate.as_view(), name="create_task"), #/tasks/add/
]
