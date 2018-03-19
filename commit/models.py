from django.db import models
from projects.models import Project
from django.utils import timezone
#from django.contrib.auth.models import User
from django.conf import settings

class CommitType(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Adap = models.IntegerField(max_length=10)
    Perfect = models.IntegerField(max_length=10)
    cor = models.IntegerField(max_length=10)
    none = models.IntegerField(max_length=10)
    date_created = models.DateTimeField(default=timezone.now)
    #def __str__(self):
     #   return self.user



'''
class RepositoryUser(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    githubid = models.CharField(max_length=100)
    gitaccesstoken = models.CharField(max_length=100)
    bitbucket = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    svn = models.CharField(max_length=100)

    #def __str__(self):
     #   return self.user
'''