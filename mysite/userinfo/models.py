from django.db import models

class UserInformation(models.Model):
	user_id = models.AutoField(primary_key=True)
	user_name = models.CharField(max_length=30)
	location = models.CharField(max_length=250)
	public_gists_count = models.PositiveIntegerField()
	public_repos_count = models.PositiveIntegerField()

class RepoInformation(models.Model):
	repo_id = models.PositiveIntegerField()
	repo_name = models.CharField(max_length=250)
	repo_url = models.URLField()
	repo_language = models.CharField(max_length=250)

class CommitInformation(models.Model):
	commit_url = models.URLField()
	commit_owner = models.CharField(max_length=30)
	commit_time = models.DateTimeField()

class UserFollerFollng(models.Model):
	user_foller_follng = models.PositiveIntegerField()