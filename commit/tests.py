# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from commit.models import CommitType
from django.test import TestCase
from django.contrib.auth.models import User
from projects.models import Project
from django.test import RequestFactory
from commit.views import git, bit, svna,pubsvn, get_image
from django.core.urlresolvers import reverse
from activities.models import Users
# Create your tests here.
class Checking_commits(TestCase):

    def create_user(self, user="Rishabh", email="abc@gmail.com", githubid="vicmassy"):
        return Users.objects.create(username=user,email=email, githubid=githubid)

    def create_user1(self, user="Rishabhq", email="ab@gmail.com", githubid="uhrishabh"):
        return Users.objects.create(username=user,email=email, bitbucket=githubid)

    def create_usr(self, user="Blecta", email="ab@gmail.com", githubid="uhrishabh"):
        return Users.objects.create(username=user, email=email, svn=githubid)

    def create_ur(self, user="Hottemaxs", email="a@gmail.com", githubid="uhrishabh"):
        return Users.objects.create(username=user, email=email, githubid=githubid)

    def create_u(self, user="Hott", email="c@gmail.com", githubid="abca"):
        return Users.objects.create(username=user, email=email, githubid=githubid)

    def test_commit_view(self):
        w = self.create_user()
        githubid="vicmassy"
        accesstoken='255b98ba03d6d3fd203d7e19b1b02de07e03975f'
        request = 'fake request'
        response = git(githubid,accesstoken)
        #self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, "Done")

    def test_commit_bitbucket(self):
        w = self.create_user1()
        githubid="uhrishabh"
        accc="acccvs"
        response = bit(githubid,"Rishabh!23")
        #self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, "Done")

    def test_commit_pubsvn(self):
        w = self.create_usr()
        githubid = "uhrishabh"
        response = pubsvn(githubid)
        #self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, "Done")

    def test_commit_svn(self):
        w = self.create_usr()
        githubid = "uhrishabh"
        url='https://svn.riouxsvn.com/lin1234/'
        response = svna(githubid,url)
        # self.assertEqual(response.status_code, 200)
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
    '''
    def test_user_creation(self):
        w = self.create_user()
        self.assertTrue(isinstance(w, Users))
        #self.assertEqual(w.__unicode__(), w.username)

    def create_project(self,name="ABC", description="abc"):
        return Project.objects.create(name=name,description=description)

    def commit_type(self,Adap="10", Perfect="5", cor="20", none="10",user="vicmassy"):
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
        github="vicmassy"
        response = get_image(github)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, "Pie chart is ready")

    def test_commit_withoutpiecard(self):
        a=self.create_user()
        w = self.commit_type()
        request = 'fake request'
        github="vicmass"
        response = get_image(github)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, "Please enter correct githubid")
