from django.contrib import admin
<<<<<<< HEAD
from projects.models import Project, UserParticipation


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')


@admin.register(UserParticipation)
class ParticipationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'project')
    list_display_links = ('id', 'user', 'project')
=======

# Register your models here.
>>>>>>> b08e6a3e8b2c2dd9bc6e05534b8e9593d0bb7dab
