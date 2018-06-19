import requests
from django.shortcuts import render
from .models import UserInformation

def index(request):

	userDataObject = {}
	if request.method == 'GET':
		username = request.GET.get('usrname')
		if not username:
			return render(request, 'index.html')
		else:
			userDataObject = UserInformation.objects.filter(username__icontains=username)
			return render(request, 'index.html', userDataObject)

	if request.method == 'POST':
		print ("Hurrah!")
		username = request.POST.get('usrname')
		userInfoUrl = 'https://api.github.com/users/' + username
		responseUserInfo = requests.get(userInfoUrl).json()

		#Getting info from API
		userInfo = {
		'usrnm' : username,
		'name' : responseUserInfo['name'],
		'location' : responseUserInfo['location'],
		'publicGistsCount' : responseUserInfo['public_gists'],
		'publicReposCount' : responseUserInfo['public_repos'],
		}

		#Saving to the database
		userinformation = UserInformation(
			usr_nm = userInfo['usrnm'],
			user_name = userInfo['name'],
			location = userInfo['location'],
			public_gists_count = userInfo['publicGistsCount'],
			public_repos_count = userInfo['publicReposCount'])
		
		userinformation.save()

		userDataObject = {'usr_info' : userInfo}
		print (userDataObject)	
		return render(request, "index.html", userDataObject)
		#return render(request, "/?username=userInfo['usrnm']")