from django.db import models
from datetime import datetime

class UserInformation(models.Model):
	usr_nm = models.CharField(max_length=30)
	user_name = models.CharField(max_length=30)
	location = models.CharField(max_length=250)
	public_gists_count = models.PositiveIntegerField()
	public_repos_count = models.PositiveIntegerField()
	created_at = models.DateTimeField(default=datetime.now, blank=True)

	def __str__(self):
		return self.usr_nm

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