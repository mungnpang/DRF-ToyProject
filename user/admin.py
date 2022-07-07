from django.contrib import admin
from django.contrib.auth.models import Group

from user.models import User as UserModel

# Register your models here.

admin.site.unregister(Group)

class idcheck(admin.ModelAdmin):
    list_display = ('id', 'name')

admin.site.register(UserModel)
