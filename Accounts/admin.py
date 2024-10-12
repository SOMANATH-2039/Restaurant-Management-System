from django.contrib import admin
from django.contrib.auth.models import User
from . models import Profile

admin.site.register(Profile)
# Mix profile info and user info

class ProfieInine(admin.StackedInline):
    model = Profile

#Extend User model

class UserAdmin(admin.ModelAdmin):
    model=User
    field=['username','password','first_name','last_name','email']
    inlines=[ProfieInine]

#Unregister the default way

admin.site.unregister(User)
admin.site.register(User,UserAdmin)