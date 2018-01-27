from django.db import models
#from activities.models import Activity
from projects.models import Project
from django.utils import timezone
from django.contrib.auth.models import User


class CommitType(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    Adap = models.IntegerField(max_length=10)
    Perfect = models.IntegerField(max_length=10)
    cor = models.IntegerField(max_length=10)
    none = models.IntegerField(max_length=10)
    date_created = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.user


'''
class CommitProjectType(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    projectname = models.ForeignKey(Project, on_delete=models.CASCADE)
    Adap = models.IntegerField(max_length=10)
    Perfect = models.IntegerField(max_length=10)
    cor = models.IntegerField(max_length=10)
    none = models.IntegerField(max_length=10)

    def __str__(self):
        return self.user
'''