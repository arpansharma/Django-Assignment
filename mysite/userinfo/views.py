import requests
from django.shortcuts import render
from .models import UserInformation

def index(request):

    userDataObject = {}
    if request.method == 'GET':
        username = request.GET.get('usrname')
        if not username:
            return render(request, 'index.html')

    elif request.method == 'POST':
        username = request.POST.get('usrname')

        #returns a query set
        userinformation = UserInformation.objects.filter(usr_nm__iexact=username)
        if not userinformation:
            userInfoUrl = 'https://api.github.com/users/' + username
            responseUserInfo = requests.get(userInfoUrl)
            #converted using request json method
            if responseUserInfo.status_code == 200:
                responseUserInfo = responseUserInfo.json()
            else:
                userData = {'error' :  "No such user found!"}
                return render(request, 'index.html', userData)

            #Getting info from API
            userInfo = {
            'usrnm' : username,
            'name' : responseUserInfo['name'],
            'location' : responseUserInfo['location'],
            'publicGistsCount' : responseUserInfo['public_gists'],
            'publicReposCount' : responseUserInfo['public_repos'],
            'followers' : responseUserInfo['followers'],
            'following' : responseUserInfo['following'],
            }

            #Saving to the database
            userinformation = UserInformation(
                usr_nm = userInfo['usrnm'],
                user_name = userInfo['name'],
                location = userInfo['location'],
                public_gists_count = userInfo['publicGistsCount'],
                public_repos_count = userInfo['publicReposCount'])
            
            userinformation.save()
        else:
            userinformation = userinformation[0]

        userData = {'usr_info' : userinformation.__dict__}
        return render(request, 'index.html', userData)
