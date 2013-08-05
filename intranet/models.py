from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from datetime import datetime
from bbhs.settings import endOfYear

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    eventsNeeded = models.IntegerField(null=True, default=4)
    eventsInfo = models.TextField(null=True, blank=True)

    eventsNeeded.verbose_name = '(Chaperone) Events Needed'
    eventsDone = models.IntegerField(null=True, default=0)
    canAdminEvents = models.BooleanField(default=False)
    isFaculty = models.BooleanField(default=False) # for do/don't send obligation emails
#    chaperone_admin

    def __unicode__(self):
        return self.user.get_full_name() or self.user.username

    def save(self, *args, **kwargs):
        try:
            existing = UserProfile.objects.get(user=self.user)
            self.id = existing.id #force update instead of insert
        except UserProfile.DoesNotExist:
            pass 
        models.Model.save(self, *args, **kwargs)

    def get_absolute_url(self):
        return '/user/%s' % self.user.username

    def daysLeft(self, _endOfYear=endOfYear):
        now = datetime.now()
        return (_endOfYear - now).days

    def eventsCompleted(self):
        completed = 4 - self.eventsNeeded
        return completed        


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
