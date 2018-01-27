# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from projects.models import Project,UserParticipation
from activities.models import Activity,Entity,Group
from measurements.models import Measurement
from django.contrib.auth.models import User
from commit.models import CommitType
import re
import json
import requests
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
import gensim
import pickle
import collections
from pylab import *
import warnings
warnings.filterwarnings("ignore")

class MeanEmbeddingVectorizer(object):
    def __init__(self, word2vec):
        self.word2vec = word2vec
        # if a text is empty we should return a vector of zeros
        # with the same dimensionality as all the other vectors
        self.dim = len(word2vec.itervalues().next())

    def fit(self, X, y):
        return self

    def transform(self, X):
        return np.array([
            np.mean([self.word2vec[w] for w in words if w in self.word2vec]
                    or [np.zeros(self.dim)], axis=0)
            for words in X
        ])

def count_user_commits(user):
    r = requests.get('https://api.github.com/users/%s/repos' % user)
    repos = json.loads(r.content)

    for repo in repos:
        if repo['fork'] is True:
            # skip it
            continue
        n = count_repo_commits(repo['url'] + '/commits')
        repo['num_commits'] = n
        yield repo


def count_repo_commits(commits_url, _acc=0):
    r = requests.get(commits_url)
    commits = json.loads(r.content)
    n = len(commits)
    if n == 0:
        return _acc
    link = r.headers.get('link')
    if link is None:
        return _acc + n
    next_url = find_next(r.headers['link'])
    if next_url is None:
        return _acc + n
    # try to be tail recursive, even when it doesn't matter in CPython
    return count_repo_commits(next_url, _acc + n)


# given a link header from github, find the link for the next url which they use for pagination
def find_next(link):
    for l in link.split(','):
        a, b = l.split(';')
        if b.strip() == 'rel="next"':
            return a.strip()[1:-1]

def wordfeatures(message):
    #stoplist=stopwords.words('english')
    X=[[word for word in line.split()] for line in message]
    x = pickle.load(open("commit/w2v.sav", 'rb'))
    Z=MeanEmbeddingVectorizer(x)
    Z1=Z.transform(X)
    return Z1

def predict(X):
    filename = 'commit/Random_model.sav'
    model= pickle.load(open(filename, 'rb'))
    print X.shape
    Y=model.predict(X)
    return Y

def label(X):
    Y=predict(X)
    return collections.Counter(Y)


def user_form(request):
    return render(request, 'commit/user_form.html')

def search(github):
    u=User.objects.get(githubid=github)
    if Group.objects.filter(name="Commit").exists():
        g = Group.objects.get(name="Commit")
    else:
        Group(name="Commit").save()
        g = Group.objects.get(name="Commit")
    if Entity.objects.filter(name="Commit",group=g).exists():
        e = Entity.objects.get(name="Commit")
    else:
        Entity(name="Commit", group=g).save()
        e = Entity.objects.get(name="Commit")
    if Activity.objects.filter(comments="Commit").exists():
        a = Activity.objects.get(comments="Commit")
    else:
        Activity(comments="Commit",entity=e).save()
        a = Activity.objects.get(comments="Commit")
    message=[]
    count=0
    adap=0
    per=0
    cor=0
    non=0
    #url = repo['url']
    for repo in count_user_commits(github):
        if Project.objects.filter(name=repo['name']).exists():
            pr = Project.objects.get(name=repo['name'])
            UserParticipation(user=u, project=pr).save()
        else:
            p = Project(name=repo['name'], description=repo['name'])
            p.save()
            pr = Project.objects.get(name=repo['name'])
            UserParticipation(user=u, project=pr)
        r = json.loads(requests.get(repo['commits_url'][:-6]).content)
        #print len(r)
        for i in range(0, len(r)):
            if Measurement.objects.filter(value=r[i]['sha']).exists():
                #message.append(re.sub('\n', ' ', r[i]['commit']['message']).encode('utf-8', 'ignore'))
                continue
            else:
                count=count+1
                p = Measurement(activity=a,type="char",name="Commit", value=r[i]['sha'] )
                p.save()
                message.append(re.sub('\n',' ',r[i]['commit']['message']).encode('utf-8', 'ignore'))

    #return HttpResponse("Done")
        #else:
         #   return HttpResponse("Enter Github ID")

def chart(request):
    return render(request, 'commit/chart.html')

def get_image(request,gitid):
    #gitid = request.POST.get('q', '')
    if User.objects.filter(githubid=gitid).exists():
        i=User.objects.get(githubid=gitid)
   #for i in range(1, len(number) + 1):
        user = CommitType.objects.filter(user=i).values("Adap")
        user = list(user)
        user1 = user[0]['Adap']
        user = CommitType.objects.filter(user=i).values("Perfect")
        user = list(user)
        user2 = user[0]['Perfect']
        user = CommitType.objects.filter(user=i).values("cor")
        user = list(user)
        user3 = user[0]['cor']
        user = CommitType.objects.filter(user=i).values("none")
        user = list(user)
        user4 = user[0]['none']
        l = ["Adaptive","Prefective", "Corrective", "None"]
        values = [user1, user2, user3, user4]
        colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
        fig = plt.figure()
    # Plot
        patches, texts = plt.pie(values, colors=colors, shadow=True, startangle=140)
        plt.legend(patches, l, loc="best")
        plt.axis('equal')
    #plt.show()
        fig.savefig("Pie chart/"+gitid+".png", bbox_inches='tight')
        return HttpResponse("Pie chart is ready")
    else:
        return HttpResponse("Please enter correct githubid")