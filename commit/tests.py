# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from commit.models import CommitType
from django.test import TestCase
from django.contrib.auth.models import User
from projects.models import Project
from django.test import RequestFactory
from commit.views import search, get_image
from django.core.urlresolvers import reverse

# Create your tests here.
class Checking_commits(TestCase):

    def create_user(self, user="Rishabh123", githubid="Hrishabh95"):
        return User.objects.create(username=user, githubid=githubid)

    def test_commit_view(self):
        w = self.create_user()
        request = 'fake request'
        response = search(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, "Done")

    def test_user_creation(self):
        w = self.create_user()
        self.assertTrue(isinstance(w, User))
        self.assertEqual(w.__unicode__(), w.username)

    def create_project(self,name="ABC", description="abc", url="http://abc.com"):
        return Project.objects.create(name=name,description=description,url=url)

    def commit_type(self,Adap="10", Perfect="5", cor="20", none="10",user="Hrishabh95"):
        i = User.objects.get(githubid=user)
        return CommitType.objects.create(Adap=Adap,Perfect=Perfect,cor=cor,none=none,user=i)

    def test_Project_creation(self):
        w=self.create_project()
        self.assertTrue(isinstance(w,Project))
        self.assertEqual(w.name, w.name)

    def test_commit_piecard(self):
        a=self.create_user()
        w = self.commit_type()
        request = 'fake request'
        github="Hrishabh95"
        response = get_image(request,github)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, "Pie chart is ready")

    def test_commit_withoutpiecard(self):
        a=self.create_user()
        w = self.commit_type()
        request = 'fake request'
        github="HRishabh"
        response = get_image(request,github)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, "Please enter correct githubid")

