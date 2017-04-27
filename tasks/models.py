from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

class Task(models.Model):
    title = models.CharField(max_length=250)
    description = models.CharField(max_length=500)
    user_id = models.ForeignKey(User, related_name="user_id")

    def get_absolute_url(self):
        return reverse('tasks:index')

    def __str__(self):
        return self.title + " - " + self.description