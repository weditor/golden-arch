from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Conference(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, default="")
    creator = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    holding_time = models.DateTimeField()

    def __str__(self):
        return self.name


class ConferenceTopic(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, default="")
    creator = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
