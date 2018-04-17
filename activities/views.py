import os

<<<<<<< HEAD
from django import forms
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from commit.views import git,bit,svna,pubsvn
import datetime
from activities.models import Activity, Entity,users
from activities.serializers import ActivitySerializer, UserSerializer
from projects.models import UserParticipation


class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = users
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            UserParticipation(user=user).save()
        return user


def register_view(request):
    form = None
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect(reverse('main') + '#/dashboard')
    return render(request, 'dash_react.html', {'form': form, 'anchor': 'register'})


class CustomLoginView(LoginView):
    template_name = 'dash_react.html'

    def get_context_data(self, **kwargs):
        context = super(CustomLoginView, self).get_context_data(**kwargs)
        if not context['form'].is_valid():
            context['anchor'] = 'login'
        return context

=======
from activities.models import Users
from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import tkinter
from tkinter import simpledialog
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from commit.views import git,bit,svna,pubsvn
from activities.models import Activity, Entity
from activities.serializers import ActivitySerializer, UserSerializer, EntitySerializer
from projects.models import UserParticipation
import datetime
>>>>>>> b08e6a3e8b2c2dd9bc6e05534b8e9593d0bb7dab

class DownloadList(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, path=None, format=None):
        if not path:
            return render(
                request,
                'activities/installer.html'
            )
        else:
            file_path = os.path.join('downloadables/', path)
            if os.path.exists(file_path):
                with open(file_path, 'rb') as fh:
                    response = HttpResponse(fh.read(), content_type="application/octet-stream")
                    response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                    return response
            else:
                return Http404()


class UserList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
<<<<<<< HEAD
    queryset = users.objects.all()
=======
    queryset = Users.objects.all()
>>>>>>> b08e6a3e8b2c2dd9bc6e05534b8e9593d0bb7dab
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
<<<<<<< HEAD
    queryset = users.objects.all()
=======
    queryset = Users.objects.all()
>>>>>>> b08e6a3e8b2c2dd9bc6e05534b8e9593d0bb7dab
    serializer_class = UserSerializer


class CreateUserView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
<<<<<<< HEAD
    model = users
=======
    model = Users
>>>>>>> b08e6a3e8b2c2dd9bc6e05534b8e9593d0bb7dab
    serializer_class = UserSerializer


class ActivityList(APIView):
    """
    List all activity list or create.
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    page_size = 20

    def get(self, request, format=None):
        project_id = request.data["project_id"] if "project_id" in request.data else None
        participation = UserParticipation.objects.get(user=request.user.id, project=project_id)
        activities = Activity.objects.filter(participation=participation)
        paginator = Paginator(activities, self.page_size)
        page = request.GET.get('page')
        try:
            res = paginator.page(page)
        except PageNotAnInteger:
            res = paginator.page(1)
        except EmptyPage:
            res = paginator.page(paginator.num_pages)

        serializer = ActivitySerializer(res, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        noErrors = True
        serializers = []
        brokenSerializers = []
<<<<<<< HEAD
        usr = users.objects.filter(username=request.user).values('time')
        now = datetime.datetime.now().replace(tzinfo=None)
        if usr[0]['time']:
            c = usr[0]['time'].replace(tzinfo=None) - datetime.datetime.now().replace(tzinfo=None)
            diff = divmod(c.days * 86400 + c.seconds, 60)
            if diff[0] > 60:
                gitid = users.objects.filter(username=request.user).values('githubid')
                bitid = users.objects.filter(username=request.user).values('bitbucket')
                svnid = users.objects.filter(username=request.user).values('svn')
                urls = users.objects.filter(username=request.user).values('urls')
=======
        usr=Users.objects.filter(username=request.user).values('time')
        now = datetime.datetime.now().replace(tzinfo=None)
        if usr[0]['time']:
            c=usr[0]['time'].replace(tzinfo=None) - datetime.datetime.now().replace(tzinfo=None)
            diff=divmod(c.days * 86400 + c.seconds, 60)
            if diff[0]>60:
                gitid = Users.objects.filter(username=request.user).values('githubid')
                bitid = Users.objects.filter(username=request.user).values('bitbucket')
                svnid = Users.objects.filter(username=request.user).values('svn')
                urls = Users.objects.filter(username=request.user).values('urls')
>>>>>>> b08e6a3e8b2c2dd9bc6e05534b8e9593d0bb7dab
                if gitid[0]['githubid']:
                    git(gitid[0]['githubid'])
                if bitid[0]['bitbucket']:
                    bit(bitid[0]['bitbucket'])
                if svnid[0]['svn'] and urls[0]['urls']:
                    svna(svnid[0]['svn'], urls[0]['urls'])
<<<<<<< HEAD
                else:
                    pubsvn(svnid[0]['svn'])
                users.objects.filter(username=request.user).update(time=now)
        else:
            users.objects.filter(username=request.user).update(time=now)
            gitid = users.objects.filter(username=request.user).values('githubid')
            bitid = users.objects.filter(username=request.user).values('bitbucket')
            svnid = users.objects.filter(username=request.user).values('svn')
            urls = users.objects.filter(username=request.user).values('urls')
=======
                if svnid[0]['svn']:
                    pubsvn(svnid[0]['svn'])
                Users.objects.filter(username=request.user).update(time=now)
        else:
            Users.objects.filter(username=request.user).update(time=now)
            gitid = Users.objects.filter(username=request.user).values('githubid')
            bitid = Users.objects.filter(username=request.user).values('bitbucket')
            svnid = Users.objects.filter(username=request.user).values('svn')
            urls = Users.objects.filter(username=request.user).values('urls')
>>>>>>> b08e6a3e8b2c2dd9bc6e05534b8e9593d0bb7dab
            if gitid[0]['githubid']:
                git(gitid[0]['githubid'])
            if bitid[0]['bitbucket']:
                bit(bitid[0]['bitbucket'])
            if svnid[0]['svn'] and urls[0]['urls']:
                svna(svnid[0]['svn'], urls[0]['urls'])
<<<<<<< HEAD
            else:
=======
            if svnid[0]['svn']:
>>>>>>> b08e6a3e8b2c2dd9bc6e05534b8e9593d0bb7dab
                pubsvn(svnid[0]['svn'])
        for data in request.data['activities']:
            user = request.user
            participation = UserParticipation.objects.get(user=user, project=None)
            entity, created = Entity.objects.get_or_create(name=data['name'])
            entity.save()
            data['participation'] = participation.id
            data['entity'] = entity.id
            serializer = ActivitySerializer(data=data)
<<<<<<< HEAD
=======
            #print user
>>>>>>> b08e6a3e8b2c2dd9bc6e05534b8e9593d0bb7dab
            noErrors = noErrors and serializer.is_valid()
            if serializer.is_valid():
                serializer.save()
                serializers.append(serializer.data)
            else:
                brokenSerializers.append(serializer)
        if noErrors:
<<<<<<< HEAD
=======
            #print git[0]['githubid']
            #search(git[0]['githubid'],acces[0]['accesstoken'])
>>>>>>> b08e6a3e8b2c2dd9bc6e05534b8e9593d0bb7dab
            return Response(
                {'activities': serializers},
                status=status.HTTP_201_CREATED
            )
        else:
            print("Error when inserting new data accured with this tuples:" +
                  repr(brokenSerializers)
                  )
            return Response(
                {'activities': serializer},
                status=status.HTTP_400_BAD_REQUEST
            )


class ActivityDetail(APIView):
    """
    Retrieve, update or delete an activity.
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_object(request, pk):
        try:
            return Activity.objects.get(pk=pk)
        except Activity.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format=None):
        activity = self.get_object(pk)
        serializer = ActivitySerializer(activity)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        activity = self.get_object(pk)
        serializer = ActivitySerializer(activity, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        activity = self.get_object(pk)
        activity.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
