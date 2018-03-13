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
import svn.remote
from datetime import datetime
from activities.models import Users
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
'''
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

'''
def count_user_commits(accesstoken):
    r = requests.get('https://api.github.com/user/repos?access_token=%s' % accesstoken)

    repos = json.loads(r.content)

    for repo in repos:
        n = count_repo_commits(repo['commits_url'][:-6])
        repo['num_commits'] = n
        yield repo


def bitbuckted_project(user):
    r = requests.get("https://api.bitbucket.org/2.0/repositories/%s" % user)
    repos = json.loads(r.content)
    A=[]
    for i in repos['values']:
        A.append(i['name'])
    return A
        #print i['name']


def bitbuckted_commit(user):
    r = requests.get("https://api.bitbucket.org/2.0/repositories/%s" % user)
    repos = json.loads(r.content)
    A = []
    mes=[]
    date=[]
    branch=[]
    for i in repos['values']:
        r = requests.get(i['links']['commits']['href'])
        r = json.loads(r.content)
        for j in r['values']:
            st = requests.get(j['links']['statuses']['href'])
            st = json.loads(st.content)
            if len(st['values']) == 0:
                branch.append('master')
            else:
                branch.append(str(st['values'][0]['description']).split(":")[1])
            A.append(j['hash'])
            mes.append(j['message'])
            date.append(j['date'])
    return A,mes,date,branch
    # print i['name']


def count_repo_commits(commits_url, _acc=0):
    r = requests.get(commits_url)
    commits = json.loads(r.content)
    n = len(commits)
    if n == 0:
        return _acc
    link = r.headers.get('link')
    if link is None:
        return _acc + n
    '''
    next_url = find_next(r.headers['link'])
    if next_url is None:
        return _acc + n
    # try to be tail recursive, even when it doesn't matter in CPython
    return count_repo_commits(next_url, _acc + n)
    '''

# given a link header from github, find the link for the next url which they use for pagination
'''
def find_next(link):
    for l in link.split(','):
        a, b = l.split(';')
        if b.strip() == 'rel="next"':
            return a.strip()[1:-1]
'''
'''
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
'''


def Day(name):
    if name == "Monday":
        return 1
    elif name == "Tuesday":
        return 2
    elif name == "Wednesday":
        return 3
    elif name == "Thursday":
        return 4
    elif name == "Friday":
        return 5
    elif name == "Saturday":
        return 6
    elif name == "Sunday":
        return 7


def search(github,access):
    r = requests.get('https://api.github.com/users/%s' % github)
    bit= requests.get("https://api.bitbucket.org/2.0/repositories/%s" % github)
    check = json.loads(r.content)
    bith=json.loads(bit.content)
    sv=0
    if 2 < len(bith):
        A=bitbuckted_project(github)
        u = Users.objects.get(githubid=github)
        if Group.objects.filter(name="Commit").exists():
            g = Group.objects.get(name="Commit")
        else:
            Group(name="Commit").save()
            g = Group.objects.get(name="Commit")

        if Group.objects.filter(name="Issue").exists():
            g1 = Group.objects.get(name="Issue")
        else:
            Group(name="Issue").save()
            g1 = Group.objects.get(name="Issue")

        if Entity.objects.filter(name="Commit", group=g).exists():
            e = Entity.objects.get(name="Commit")
        else:
            Entity(name="Commit", group=g).save()
            e = Entity.objects.get(name="Commit")

        if Entity.objects.filter(name="Issue", group=g1).exists():
            e1 = Entity.objects.get(name="Issue")
        else:
            Entity(name="Issue", group=g1).save()
            e1 = Entity.objects.get(name="Issue")

        if Activity.objects.filter(comments="BitBucketCommit").exists():
           a = Activity.objects.get(comments="BitBucketCommit")
        else:
            Activity(comments="BitBucketCommit", entity=e).save()
            a = Activity.objects.get(comments="BitBucketCommit")

        if Activity.objects.filter(comments="BitBucketissue").exists():
           a1 = Activity.objects.get(comments="BitBucketissue")
        else:
            Activity(comments="BitBucketissue", entity=e1).save()
            a1 = Activity.objects.get(comments="BitBucketissue")
        message = []
        count = 0
        for i in A:
            #if Project.objects.filter(name=i).exists():
             #   pr = Project.objects.get(name=i)
              #  UserParticipation(user=u, project=pr).save()
            #else:
            p = Project(name=i, description=i, url=i)
            p.save()
            pr = Project.objects.get(name=i)
            UserParticipation(user=u, project=pr)
        comm,mess,date,br=bitbuckted_commit(github)
        r = requests.get("https://api.bitbucket.org/2.0/repositories/%s" % github)
        repos = json.loads(r.content)
        for m in repos['values']:
            r = requests.get("https://api.bitbucket.org/2.0/repositories/"+github+"/"+m['name'])
            r = json.loads(r.content)
            r=json.loads(requests.get(r['links']['issues']['href']).content)
            for i in r['values']:
                if Measurement.objects.filter(value=i['id']).exists():
                    continue
                else:
                    Measurement(activity=a, type="char", name="BitBucketCommit_ID", value=i['id']).save()
                    Measurement(activity=a, type="char", name="BitBucketCommit_kind", value=i['kind']).save()
                    Measurement(activity=a, type="char", name="BitBucketCommit_name", value=i['repository']['name']).save()
                    Measurement(activity=a, type="char", name="BitBucketCommit_priority", value=i['priority']).save()
                    Measurement(activity=a, type="char", name="BitBucketCommit_title", value=i['title']).save()
        for i in range(len(comm)):
            if Measurement.objects.filter(value=comm[i]).exists():
                continue
            else:
                da = date[i].split("T")[0]
                t = date[i].split("T")[1].split('+')[0]
                da = datetime.datetime.strptime(da, '%Y-%m-%d').strftime('%A')
                if 6 <= int(t.split(":")[0]) and int(t.split(":")[0]) < 12:
                    time = 1
                elif 12 <= int(t.split(":")[0]) and int(t.split(":")[0]) < 18:
                    time = 2
                elif 18 <= int(t.split(":")[0]) and int(t.split(":")[0]) < 24:
                    time = 3
                elif 0 <= int(t.split(":")[0]) and int(t.split(":")[0]) < 6:
                    time = 4
                da = Day(da)
                Measurement(activity=a, type="char", name="BitBucketCommit_ID", value=comm[i]).save()
                Measurement(activity=a, type="char", name="BitBucketCommit_Day", value=da).save()
                Measurement(activity=a, type="char", name="BitBucketCommit_Time", value=t).save()
                Measurement(activity=a, type="char", name="BitBucketCommit_branch", value=br[i]).save()
                Measurement(activity=a, type="char", name="BitBucketCommit_message", value=mess[i]).save()
        return HttpResponse("Done")

    elif len(check) > 2:
        u = Users.objects.get(githubid=github)
        if Group.objects.filter(name="Commit").exists():
            g = Group.objects.get(name="Commit")
        else:
            Group(name="Commit").save()
            g = Group.objects.get(name="Commit")
        if Group.objects.filter(name="Issue").exists():
            gi = Group.objects.get(name="Issue")
        else:
            Group(name="Issue").save()
            gi = Group.objects.get(name="Issue")
        if Entity.objects.filter(name="Commit", group=g).exists():
            e = Entity.objects.get(name="Commit")
        else:
            Entity(name="Commit", group=g).save()
            e = Entity.objects.get(name="Commit")

        if Entity.objects.filter(name="Issue", group=gi).exists():
            ei = Entity.objects.get(name="Issue")
        else:
            Entity(name="Issue", group=gi).save()
            ei = Entity.objects.get(name="Issue")

        for repo in count_user_commits(access):
            if Project.objects.filter(name=repo['name']).exists():
                pr = Project.objects.get(name=repo['name'])
                UserParticipation(user=u, project=pr).save()
            else:
                p = Project(name=repo['name'], description=repo['name'], url=repo['url'])
                p.save()
                pr = Project.objects.get(name=repo['name'])
                UserParticipation(user=u, project=pr)
            r = json.loads(requests.get(repo['commits_url'][:-6]).content)
            r1 = json.loads(requests.get(repo['issue_comment_url'][:-9]).content)
            for k in range(0,len(r1)):
                if Measurement.objects.filter(value=r[i]['id']).exists():
                    continue
                else:
                    Activity(comments="Git Issue " + str(k) + " " + str(repo['name']), entity=ei).save()
                    a = Activity.objects.get(comments="Git Issue " + str(i) + " " + str(repo['name']))
                    Measurement(activity=a, type="char", name="Type", value="Git Issue").save()
                    Measurement(activity=a, type="char", name="GIssue_ID", value=r[i]['id']).save()
                    Measurement(activity=a, type="char", name="GIssue_ID", value=r[i]['body']).save()
            for i in range(0, len(r)):
                if Measurement.objects.filter(value=r[i]['sha']).exists():
                    continue
                else:
                    Activity(comments="Git commit " + str(i) + " " + str(repo['name']), entity=e).save()
                    a = Activity.objects.get(comments="Git commit " + str(i) + " " + str(repo['name']))
                    rr = requests.get(r[i]['url'])
                    rr = json.loads(rr.content)
                    d = rr['stats']['deletions']
                    l = rr['stats']['additions']
                    no = len(rr['files'])
                    date = rr['commit']['committer']['date'].split("T")[0]
                    t = rr['commit']['committer']['date'].split("T")[1][:-1]
                    day = datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%A')
                    if 6 <= int(t.split(":")[0]) and int(t.split(":")[0]) < 12:
                        time = 1
                    elif 12 <= int(t.split(":")[0]) and int(t.split(":")[0]) < 18:
                        time = 2
                    elif 18 <= int(t.split(":")[0]) and int(t.split(":")[0]) < 24:
                        time = 3
                    elif 0 <= int(t.split(":")[0]) and int(t.split(":")[0]) < 6:
                        time = 4
                    da = Day(day)
                    Measurement(activity=a, type="char", name="Type", value="Git Commit").save()
                    Measurement(activity=a,type='char', name="User", value=github).save()
                    Measurement(activity=a, type="char", name="Gcommit_ID", value=r[i]['sha']).save()
                    Measurement(activity=a, type="char", name="Gcommit_deletions", value=d).save()
                    Measurement(activity=a, type="char", name="Gcommit_addition", value=l).save()
                    Measurement(activity=a, type="char", name="Gcommit_nooffiles", value=no).save()
                    Measurement(activity=a, type="char", name="Gcommit_timelabel", value=time).save()
                    Measurement(activity=a, type="char", name="Gcommit_daylabel", value=da).save()
                    Measurement(activity=a, type="char", name="Gcommit_message",
                                value=re.sub('\n', ' ', r[i]['commit']['message']).encode('utf-8', 'ignore')).save()
        return HttpResponse("Done")
    elif sv==0:
        u = Users.objects.get(githubid=github)
        if Group.objects.filter(name="Commit").exists():
            g = Group.objects.get(name="Commit")
        else:
            Group(name="Commit").save()
            g = Group.objects.get(name="Commit")
        if Entity.objects.filter(name="Commit", group=g).exists():
            en = Entity.objects.get(name="Commit")
        else:
            Entity(name="Commit", group=g).save()
            en = Entity.objects.get(name="Commit")
        r = svn.remote.RemoteClient('http://svn.apache.org/repos/asf/')
        entries = r.list()
        for filename in entries:
            r = svn.remote.RemoteClient('http://svn.apache.org/repos/asf/' + filename)
            if Project.objects.filter(name=filename).exists():
                pr = Project.objects.get(name=filename)
                UserParticipation(user=u, project=pr).save()
            else:
                p = Project(name=filename, description=filename, url='http://svn.apache.org/repos/asf/' + filename)
                p.save()
                pr = Project.objects.get(name=filename)
                UserParticipation(user=u, project=pr)
            e = r.list()
            for file in e:
                if file == "trunk/":
                    a = svn.remote.RemoteClient('http://svn.apache.org/repos/asf/' + filename + "trunk")
                    i=0
                    '''
                    for log in a.log_default():
                        if log[3] == github:
                            if Measurement.objects.filter(value=log[2]).exists():
                                continue
                            else:
                                i=i+1
                                Activity(comments="SVN commit " + str(i) + " " + str(filename), entity=en).save()
                                ac = Activity.objects.get(comments="SVN commit " + str(i) + " " + str(filename))
                                Measurement(activity=ac, type="char", name="Type", value="SVN Commit").save()
                                Measurement(activity=ac, type='char', name="User", value=github).save()
                                Measurement(activity=ac, type="char", name="Scommit_ID", value=log[2]).save()
                                Measurement(activity=ac, type="char", name="Scommit_message", value=log[1]).save()
                    '''
        return HttpResponse("Done")
    else:
        return HttpResponse("Done")
    '''
    if len(check)>2 and len(bith)>2:
        u=Users.objects.get(githubid=github)
        if Group.objects.filter(name="Commit").exists():
            g = Group.objects.get(name="Commit")
        else:
            Group(name="Commit").save()
            g = Group.objects.get(name="Commit")
        if Entity.objects.filter(name="Commit", group=g).exists():
            e = Entity.objects.get(name="Commit")
        else:
            Entity(name="Commit", group=g).save()
            e = Entity.objects.get(name="Commit")
        message = []
        bitmessage=[]
        count = 0
        adap = 0
        per = 0
        cor = 0
        non = 0
        # url = repo['url']
        feat=[]
        A = bitbuckted_project(github)
        for pro in A:
            if Project.objects.filter(name=pro).exists():
                pr = Project.objects.get(name=pro)
                UserParticipation(user=u, project=pr).save()
            else:
                p = Project(name=pro, description=pro, url=pro)
                p.save()
                pr = Project.objects.get(name=pro)
                UserParticipation(user=u, project=pr)
        comm,bitmes=bitbuckted_commit(github)
        for numb in range(0,len(comm)):
            if Measurement.objects.filter(value=comm[numb]).exists():
                continue
            else:
                count = count + 1
                p = Measurement(activity=a, type="char", name="Commit on bitbucket", value=comm[numb])
                p.save()
                bitmessage.append(re.sub('\n', ' ', str(bitmes[numb]).encode('utf-8', 'ignore')))
        for repo in count_user_commits(github):
            if Project.objects.filter(name=repo['name']).exists():
                pr = Project.objects.get(name=repo['name'])
                UserParticipation(user=u, project=pr).save()
            else:
                p = Project(name=repo['name'], description=repo['name'], url = repo['url'])
                p.save()
                pr = Project.objects.get(name=repo['name'])
                UserParticipation(user=u, project=pr)
            r = json.loads(requests.get(repo['commits_url'][:-6]).content)
            for i in range(0, len(r)):
                if Measurement.objects.filter(value=r[i]['sha']).exists():
                    continue
                else:
                    Activity(comments="Git commit "+str(i)+" "+str(repo['name']), entity=e).save()
                    a = Activity.objects.get(comments="Git commit "+str(i)+" "+str(repo['name']))
                    count = count + 1
                    rr=requests.get(r[i]['url'])
                    rr=json.loads(rr.content)
                    d=rr['stats']['deletions']
                    l=rr['stats']['additions']
                    no=len(rr['files'])
                    date = rr['commit']['committer']['date'].split("T")[0]
                    t = rr['commit']['committer']['date'].split("T")[1][:-1]
                    day = datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%A')
                    if 6 <= int(t.split(":")[0]) and int(t.split(":")[0]) < 12:
                        time=1
                    elif 12 <= int(t.split(":")[0]) and int(t.split(":")[0]) < 18:
                        time=2
                    elif 18 <= int(t.split(":")[0]) and int(t.split(":")[0]) < 24:
                        time=3
                    elif 0 <= int(t.split(":")[0]) and int(t.split(":")[0]) < 6:
                        time=4
                    da=Day(day)
                    #print len(feat)
                    Measurement(activity=a, type="char", name="Type", value="Git Commit").save()
                    Measurement(activity=a, type="char", name="Gcommit_ID", value=r[i]['sha']).save()
                    Measurement(activity=a, type="char", name="Gcommit_deletions", value=d).save()
                    Measurement(activity=a, type="char", name="Gcommit_addition", value=l).save()
                    Measurement(activity=a, type="char", name="Gcommit_nooffiles", value=no).save()
                    Measurement(activity=a, type="char", name="Gcommit_timelabel", value=time).save()
                    Measurement(activity=a, type="char", name="Gcommit_daylabel", value=da).save()
                    Measurement(activity=a, type="char", name="Gcommit_message", value=re.sub('\n', ' ', r[i]['commit']['message']).encode('utf-8', 'ignore')).save()
        return HttpResponse("Done")
        
        
        if len(message) > 0:
            x = wordfeatures(message)
            lab = label(x)
            adap = adap + lab[2]
            per = per + lab[3]
            cor = cor + lab[1]
            non = non + lab[0]
            if CommitType.objects.filter(user=u).exists():
                user = CommitType.objects.filter(user=u).values("Adap")
                user = list(user)
                user1 = user[0]['Adap']
                user = CommitType.objects.filter(user=u).values("Perfect")
                user = list(user)
                user2 = user[0]['Perfect']
                user = CommitType.objects.filter(user=u).values("cor")
                user = list(user)
                user3 = user[0]['cor']
                user = CommitType.objects.filter(user=u).values("none")
                user = list(user)
                user4 = user[0]['none']
                adap = adap + user1
                per = per + user2
                cor = cor + user3
                non = non + user4
                CommitType.objects.filter(user=u).delete()
                CommitType(user=u, Adap=adap, Perfect=per, cor=cor, none=non).save()
            else:
                CommitType(user=u, Adap=adap, Perfect=per, cor=cor, none=non).save()
            l = ["Adaptive", "Prefective", "Corrective", "None"]
            values = [user1, user2, user3, user4]
            colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
            fig = plt.figure()
            # Plot
            def make_autopct(values):
                def my_autopct(pct):
                    total = sum(values)
                    val = int(round(pct * total / 100.0))
                    return '{p:.2f}%  ({v:d})'.format(p=pct, v=val)

                return my_autopct

            plt.pie(values, labels=l, autopct=make_autopct(values))
            plt.axis('equal')
            fig.savefig("Pie chart/" + github + ".png", bbox_inches='tight')
        '''
        #return HttpResponse("Done")



         #   return HttpResponse("Enter Github ID")

'''
def chart(request):
    return render(request, 'commit/chart.html')
'''

def get_image(gitid):
    #gitid = request.POST.get('q', '')
    if Users.objects.filter(githubid=gitid).exists():
        i=Users.objects.get(githubid=gitid)
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
        def make_autopct(values):
            def my_autopct(pct):
                total = sum(values)
                val = int(round(pct * total / 100.0))
                return '{p:.2f}%  ({v:d})'.format(p=pct, v=val)
            return my_autopct
        plt.pie(values, labels=l, autopct=make_autopct(values))
        plt.axis('equal')
    #plt.show()
        #fig.savefig("Pie chart/"+gitid+".png", bbox_inches='tight')
        return HttpResponse("Pie chart is ready")
    else:
        return HttpResponse("Please enter correct githubid")
