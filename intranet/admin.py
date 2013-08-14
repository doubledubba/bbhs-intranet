from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from intranet.models import UserProfile
from bbhs.settings import OBLIGATION_NUMBER

def turnOnAdmin(modelAdmin, request, querySet):
    for user in querySet:
        #user.is_staff = True
        #user.save()
        profile = user.get_profile()        
        profile.canAdminEvents = True
        profile.save()

def turnOffAdmin(modelAdmin, request, querySet):
    for user in querySet:
        #user.is_staff = False
        #user.save()
        profile = user.get_profile()
        profile.canAdminEvents = False
        profile.save()

def normalize_yearly_obligation(modelAdmin, request, querySet):
    for user in querySet:
        profile = user.get_profile()
        if not profile.user.is_active:
            continue
        profile.eventsNeeded = OBLIGATION_NUMBER
        profile.eventsDoneSoFar = 0
        profile.save()

turnOnAdmin.short_description = 'Make the user a potential admin'
turnOffAdmin.short_description = 'Remove the user\'s administration privileges'

# Define an inline admin descriptor for UserProfile model
# which acts a bit like a singleton
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'profile'

# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (UserProfileInline, )
    list_display = ['username', 'get_full_name', 'email']
    actions = [turnOnAdmin, turnOffAdmin, normalize_yearly_obligation]

    #def canAdmin(self, user):
     #   return user.get_profile().canAdminEvents and user.is_staff

    #canAdmin.short_description = 'Can admin events'
    #canAdmin.boolean = True

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

