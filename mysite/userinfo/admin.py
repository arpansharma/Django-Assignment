from django.contrib import admin
from .models import UserInformation, UserFlrFlg, RepoInformation, BranchInformation, CommitInformation

admin.site.register(UserInformation)
admin.site.register(UserFlrFlg)
admin.site.register(RepoInformation)
admin.site.register(BranchInformation)
admin.site.register(CommitInformation)