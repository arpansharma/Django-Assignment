import requests
from django.shortcuts import render
from django.forms.models import model_to_dict
from .models import UserInformation, UserFlrFlg, RepoInformation, BranchInformation, CommitInformation

def index(request):

    userDataObject = {}
    if request.method == 'GET':
        username = request.GET.get('usrname')
        if not username:
            return render(request, 'index.html')

    elif request.method == 'POST':
        # import pdb
        # pdb.set_trace()
        username = request.POST.get('usrname')

        #returns a query set
        #extraxt follower info for this userinformation
        userinformation = UserInformation.objects.filter(usr_nm__iexact=username)        
        usrflr = UserFlrFlg.objects.filter(usr_nm__iexact=username, local_id=1)
        usrflg = UserFlrFlg.objects.filter(usr_nm__iexact=username, local_id=2)
        repoinformation = RepoInformation.objects.filter(usr_nm__iexact=username)
        if not userinformation:
            userInfoUrl = 'https://api.github.com/users/' + username
            responseUserInfo = requests.get(userInfoUrl)
            #converted using request json method
            if responseUserInfo.status_code == 200:
                responseUserInfo = responseUserInfo.json()
            else:
                userData = {'error' :  "No such user found!"}
                return render(request, 'index.html', userData)

            #Getting User - Info from API
            userInfo = {
            'usrnm' : username,
            'name' : responseUserInfo.get('name') or 'NA',
            'location' : responseUserInfo.get('location') or 'NA',
            'publicGistsCount' : responseUserInfo.get('public_gists'),
            'publicReposCount' : responseUserInfo.get('public_repos'),
            'followers' : responseUserInfo.get('followers'),
            'following' : responseUserInfo.get('following'),
            }

            #Saving to the database
            userinformation = UserInformation(
                usr_nm = userInfo['usrnm'],
                user_name = userInfo['name'],
                location = userInfo['location'],
                public_gists_count = userInfo['publicGistsCount'],
                public_repos_count = userInfo['publicReposCount'])
            
            userinformation.save()


            #Getting Follower - Info from API
            frInfoUrl = 'https://api.github.com/users/' + username + '/followers'
            responsefr_info = requests.get(frInfoUrl).json()
            # import pdb;pdb.set_trace()
            usrflrlist= []
            for value in responsefr_info:                              
                usrflr = UserFlrFlg(usr_nm = username, name = value['login'], local_id = 1)                
                usrflr.save()
                usrflrlist.append(model_to_dict(usrflr))

            #Getting Following - Info from API
            fgInfoUrl = 'https://api.github.com/users/' + username + '/following'
            responsefg_info = requests.get(fgInfoUrl).json()
            usrflglist = []         
            for value in responsefg_info:                              
                usrflg = UserFlrFlg(usr_nm = username, name = value['login'], local_id = 2)                
                usrflg.save()
                usrflglist.append(model_to_dict(usrflg))

            #Getting Repositories - Info from API
            repoInfoUrl = 'https://api.github.com/users/' + username + '/repos'
            responserepo_info = requests.get(repoInfoUrl).json()
            repoinformationlist = []       
            for r_value in responserepo_info:                              
                repoinformation = RepoInformation(
                usr_nm = username,
                repo_name = r_value['name'],
                repo_url = r_value['html_url'],
                repo_language = r_value.get('language') or 'NA')
                repoinformation.save()
                repoinformationlist.append(model_to_dict(repoinformation))

        else:
            userinformation = userinformation[0]
            usrflrlist = []
            usrflglist = []
            repoinformationlist = []
            for value in usrflr:
                usrflrlist.append(model_to_dict(value))
            for value in usrflg:
                usrflglist.append(model_to_dict(value))
            for value in repoinformation:
                repoinformationlist.append(model_to_dict(value))

        userData = {
        'usr_info': userinformation.__dict__,
        'fr_info': usrflrlist,
        'fg_info': usrflglist,
        'repo_info': repoinformationlist
        }

        return render(request, 'index.html', userData)

def repo(request):
    if request.method == 'GET':
        #Getting Branch - Info from API
        #https://api.github.com/repos/arpansharma/Android-Linux-Server-Connectivity/branches
        repo_id = request.GET.get('repo_id')
        if repo_id:
            repo = RepoInformation.objects.filter(id=repo_id)
            if repo:
                repo = repo[0]
                branchinformation = BranchInformation.objects.filter(repo_name=repo.repo_name)
                if not branchinformation:
                    branchInfoUrl = 'https://api.github.com/repos/' + repo.usr_nm + '/' + repo.repo_name + '/branches'
                    responsebranch_info = requests.get(branchInfoUrl).json()
                    branchinformationlist = []
                    for b_value in responsebranch_info:
                        branchinformation = BranchInformation(    
                        usr_nm = repo.usr_nm,                    
                        repo_name = repo.repo_name,
                        branch_name = b_value['name'])
                        branchinformation.save()
                        branchinformationlist.append(model_to_dict(branchinformation))                        
                else:
                    branchinformationlist = []
                    for value in branchinformation:
                        branchinformationlist.append(model_to_dict(value))

                data = {
                    'repo_info': repo,
                    'branch_info': branchinformationlist
                }
                return render(request, 'repo.html', data)

            else:
                return render(request, 'repo.html')
        else:
            return render(request, 'repo.html')

def branch(request):
    if request.method == 'GET':
        branch_id = request.GET.get('branch_id')
        if branch_id:
            branch = BranchInformation.objects.filter(id=branch_id)
            if branch:
                branch = branch[0]
                commitinformation = CommitInformation.objects.filter(branch_name=branch.branch_name)
                if not commitinformation:
                    # Getting Commit - Info from API
                    # https://api.github.com/repos/arpansharma/Android-Linux-Server-Connectivity/commits/
                    commitInfoUrl = 'https://api.github.com/repos/' + branch.usr_nm + '/' + branch.repo_name + '/commits'
                    print (commitInfoUrl)
                    responsecommit_info = requests.get(commitInfoUrl).json()
                    commitinformationlist = []
                    for c_value in responsecommit_info:
                        commitinformation = CommitInformation(
                        branch_name = branch.branch_name,
                        commit_url = c_value['html_url'],
                        commit_message = c_value['commit']['message'],                        
                        commit_author = c_value['commit']['author']['name'],
                        commit_date = c_value['commit']['author']['date'])
                        commitinformation.save()
                        print (commitinformation)
                        commitinformationlist.append(model_to_dict(commitinformation))                        
                else:
                    commitinformationlist = []
                    for value in commitinformation:
                        commitinformationlist.append(model_to_dict(value))

                data = {
                    'branch_info' : branch,                    
                    'commit_info': commitinformationlist
                }
                return render(request, 'branch.html', data)

            else:
                return render(request, 'branch.html')
        else:
            return render(request, 'branch.html')

def commit(request):
    if request.method == 'GET':
        commit_id = request.GET.get('commit_id')
        if commit_id:
            return render(request, 'commit.html')