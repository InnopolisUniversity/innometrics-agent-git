import os

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
    queryset = Users.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Users.objects.all()
    serializer_class = UserSerializer


class CreateUserView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    model = Users
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
                if gitid[0]['githubid']:
                    git(gitid[0]['githubid'])
                if bitid[0]['bitbucket']:
                    bit(bitid[0]['bitbucket'])
                if svnid[0]['svn'] and urls[0]['urls']:
                    svna(svnid[0]['svn'], urls[0]['urls'])
                if svnid[0]['svn']:
                    pubsvn(svnid[0]['svn'])
                Users.objects.filter(username=request.user).update(time=now)
        else:
            Users.objects.filter(username=request.user).update(time=now)
            gitid = Users.objects.filter(username=request.user).values('githubid')
            bitid = Users.objects.filter(username=request.user).values('bitbucket')
            svnid = Users.objects.filter(username=request.user).values('svn')
            urls = Users.objects.filter(username=request.user).values('urls')
            if gitid[0]['githubid']:
                git(gitid[0]['githubid'])
            if bitid[0]['bitbucket']:
                bit(bitid[0]['bitbucket'])
            if svnid[0]['svn'] and urls[0]['urls']:
                svna(svnid[0]['svn'], urls[0]['urls'])
            if svnid[0]['svn']:
                pubsvn(svnid[0]['svn'])
        for data in request.data['activities']:
            user = request.user
            participation = UserParticipation.objects.get(user=user, project=None)
            entity, created = Entity.objects.get_or_create(name=data['name'])
            entity.save()
            data['participation'] = participation.id
            data['entity'] = entity.id
            serializer = ActivitySerializer(data=data)
            #print user
            noErrors = noErrors and serializer.is_valid()
            if serializer.is_valid():
                serializer.save()
                serializers.append(serializer.data)
            else:
                brokenSerializers.append(serializer)
        if noErrors:
            #print git[0]['githubid']
            #search(git[0]['githubid'],acces[0]['accesstoken'])
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
