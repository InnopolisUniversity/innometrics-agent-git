from django.db import models
from django.contrib.auth.models import User


class users(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    githubid = models.CharField(max_length=30, blank=True, null=True)
    bitbucket = models.CharField(max_length=100, blank=True, null=True)
    svn = models.CharField(max_length=100, blank=True, null=True)
    urls = models.CharField(max_length=10000, blank=True, null=True)
    time = models.DateTimeField(null=True)