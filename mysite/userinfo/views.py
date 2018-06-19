import requests
from django.shortcuts import render
from .models import UserInformation

def index(request):
	
	if request.method == 'POST':
		print ("Hurrah!")
		username = request.POST.get('usrname')
		userInfoUrl = 'https://api.github.com/users/' + username
		responseUserInfo = requests.get(userInfoUrl).json()

		userInfo = {
		'name' : responseUserInfo['name'],
		'location' : responseUserInfo['location'],
		'publicGistsCount' : responseUserInfo['public_gists'],
		'publicReposCount' : responseUserInfo['public_repos'],
		}

		userinformation = UserInformation(
			user_name = userInfo['name'],
			location = userInfo['location'],
			public_gists_count = userInfo['publicGistsCount'],
			public_repos_count = userInfo['publicReposCount'])
		
		userinformation.save()

	return render(request, 'index.html')