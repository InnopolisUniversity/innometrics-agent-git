<<<<<<< HEAD
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.conf import settings


class Project(models.Model):
    name = models.CharField(max_length=150, blank=True)
    description = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return self.name


class UserParticipation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True, null=True, related_name='participations')

    def __str__(self):
        return str(self.user) + " - " + str(self.project)


class Metric(models.Model):
    name = models.CharField(max_length=255, blank=True)
    participation = models.ForeignKey(UserParticipation, on_delete=models.CASCADE)
    RAW = 'R'
    COMPOSITE = 'C'
    METRIC_TYPE_CHOICES = (
        (RAW, 'raw'),
        (COMPOSITE, 'composite')
    )
    type = models.CharField(max_length=1, choices=METRIC_TYPE_CHOICES)
    info = JSONField()

    def __str__(self):
        return str(self.participation) + " - " + self.name
=======
from django.db import models
#from activities.models import Users
from django.conf import settings

class Project(models.Model):
    name = models.CharField(max_length=150, blank=True)
    description = models.CharField(max_length=150, blank=True)
    url=models.CharField(max_length=100,blank=True)

class UserParticipation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True, null=True)
>>>>>>> b08e6a3e8b2c2dd9bc6e05534b8e9593d0bb7dab
