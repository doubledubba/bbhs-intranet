from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from datetime import datetime
import json
from bbhs.settings import endOfYear, OBLIGATION_NUMBER

class Action(object):
    def __init__(self, **kwargs):
        for arg in kwargs:
            setattr(self, arg, kwargs[arg])


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    eventsNeeded = models.IntegerField(null=True, default=OBLIGATION_NUMBER)
    #eventsNeeded reset yearly
    eventsInfo = models.TextField(null=True, blank=True)

    eventsNeeded.verbose_name = '(Chaperone) Events Needed'
    eventsDone = models.IntegerField(null=True, default=0) #permanent tally
    eventsDoneSoFar = models.IntegerField(null=True, default=0)
    eventsDoneSoFar.description = 'Events Dun So Far'

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

    def rtEventsNeeded(self):
        return self.eventsNeeded if self.eventsNeeded > 0 else 0

    def daysLeft(self, _endOfYear=endOfYear):
        now = datetime.now()
        return (_endOfYear - now).days

    def logAction(self, action, event):
        now = datetime.now()
        if action == 'sign up':
            action = 0
        elif action == 'unsign up':
            action = 1
        params = [
            action,
            now.strftime('%c'),
            event.pk,
            event.name,
            event.weight,
        ]
        entry = json.dumps(params)
        if self.eventsInfo:
            log = json.loads(self.eventsInfo)
        else:
            log = []
        log.append(entry)
        self.eventsInfo = json.dumps(log)
        self.save()
            

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
