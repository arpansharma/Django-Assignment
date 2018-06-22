from django.db import models
from datetime import datetime

class UserInformation(models.Model):
	usr_nm = models.CharField(max_length=30)
	user_name = models.CharField(max_length=30)
	location = models.CharField(max_length=250)
	public_gists_count = models.PositiveIntegerField()
	public_repos_count = models.PositiveIntegerField()
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.usr_nm

class RepoInformation(models.Model):
	#repo_id = models.ForeignKey(UserInformation, on_delete=models.CASCADE)
	usr_nm = models.CharField(max_length=30)
	repo_name = models.CharField(max_length=250)
	repo_url = models.URLField()
	repo_language = models.CharField(max_length=250)

	def __str__(self):
		return self.repo_name

class BranchInformation(models.Model):
	#branch_id = models.ForeignKey(RepoInformation, on_delete=models.CASCADE)
	usr_nm = models.CharField(max_length=30)
	repo_name = models.CharField(max_length=250)
	branch_name = models.CharField(max_length=30)

	def __str__(self):
		return self.repo_name

class CommitInformation(models.Model):
	#commit_id = models.ForeignKey(BranchInformation, on_delete=models.CASCADE)
	repo_name = models.CharField(max_length=250)
	branch_name = models.CharField(max_length=30)
	commit_message = models.CharField(max_length=250)
	commit_url = models.URLField()
	commit_author = models.CharField(max_length=30)
	commit_date = models.DateTimeField()

	def __str__(self):
		return self.commit_url

# UserFlrFlg = UserFollowerFollowing
class UserFlrFlg(models.Model):
	#flrflg_id = models.ForeignKey(UserInformation, on_delete=models.CASCADE)
	usr_nm = models.CharField(max_length=30)
	local_id = models.PositiveIntegerField()
	# 1 = Follower, 2 = Following
	name = models.CharField(max_length=30)

	def __str__(self):
		return self.usr_nm
