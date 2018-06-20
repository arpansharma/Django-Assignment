from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('repo/', views.repo, name='repo'),
	path('', views.branch, name='branch'),
	path('', views.commit, name='commit'),
]