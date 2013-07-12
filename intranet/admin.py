from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from intranet.models import UserProfile

def turnOnAdmin(modelAdmin, request, querySet):
    for user in querySet:
        profile = user.get_profile()
        profile.canAdminEvents = True
        profile.save()

def turnOffAdmin(modelAdmin, request, querySet):
    for user in querySet:
        profile = user.get_profile()
        profile.canAdminEvents = False
        profile.save()

turnOnAdmin.short_description = 'Make the user a potential admin'
turnOffAdmin.short_description = 'Remove the user\'s administration priviledges'

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
    actions = [turnOnAdmin, turnOffAdmin]


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

