# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from commit.models import CommitType
from django.test import TestCase
from django.contrib.auth.models import User
from projects.models import Project
from django.test import RequestFactory
from commit.views import search, get_image
from django.core.urlresolvers import reverse
from activities.models import Users
# Create your tests here.
class Checking_commits(TestCase):

    def create_user(self, user="Rishabh", email="abc@gmail.com", githubid="Hrishabh95",accesstoken="10e9a94541ab7cd3371ad18077fb77a3f34b6c4e"):
        return Users.objects.create(username=user,email=email, githubid=githubid, accesstoken=accesstoken)

    def create_user1(self, user="Rishabhq", email="ab@gmail.com", githubid="vicmass",accesstoken="abcsds"):
        return Users.objects.create(username=user,email=email, githubid=githubid, accesstoken=accesstoken)

    def create_usr(self, user="Blecta", email="ab@gmail.com", githubid="Nicksaurus",accesstoken='acccvs'):
        return Users.objects.create(username=user, email=email, githubid=githubid, accesstoken=accesstoken)

    def create_ur(self, user="Hottemaxs", email="a@gmail.com", githubid="Hottemax"):
        return Users.objects.create(username=user, email=email, githubid=githubid)

    def create_u(self, user="Hott", email="c@gmail.com", githubid="abca"):
        return Users.objects.create(username=user, email=email, githubid=githubid)

    def test_commit_view(self):
        w = self.create_user()
        githubid="Hrishabh95"
        accesstoken='10e9a94541ab7cd3371ad18077fb77a3f34b6c4e'
        request = 'fake request'
        response = search(githubid,accesstoken)
        #self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, "Done")

    '''
    def test_commit_bitbucket(self):
        w = self.create_usr()
        githubid="Nicksaurus"
        accc="acccvs"
        response = search(githubid,accc)
        #self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, "Done")
    
    def test_commit_Gitnbitbucket(self):
        w = self.create_ur()
        githubid = "Hottemax"
        response = search(githubid)
        #self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, "Done")
    
    '''
    def test_commit_wrong_view(self):
        w = self.create_user1()
        githubid="vicmass"
        acc="abcsds"
        response = search(githubid,acc)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, "Done")


    def test_commit_wrong_(self):
        w = self.create_u()
        githubid="abca"
        acc="avc"
        response = search(githubid,acc)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, "Done")

    def test_user_creation(self):
        w = self.create_user()
        self.assertTrue(isinstance(w, Users))
        #self.assertEqual(w.__unicode__(), w.username)

    def create_project(self,name="ABC", description="abc"):
        return Project.objects.create(name=name,description=description)

    def commit_type(self,Adap="10", Perfect="5", cor="20", none="10",user="Hrishabh95"):
        i = Users.objects.get(githubid=user)
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
        response = get_image(github)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, "Pie chart is ready")

    def test_commit_withoutpiecard(self):
        a=self.create_user()
        w = self.commit_type()
        request = 'fake request'
        github="HRishabh"
        response = get_image(github)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, "Please enter correct githubid")
