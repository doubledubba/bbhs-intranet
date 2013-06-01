import json
from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import utc
from intranet.models import UserProfile

class Event(models.Model):
    name = models.CharField(max_length=80)
    admin = models.ForeignKey(User)
    date = models.DateTimeField()
    volunteersNeeded = models.IntegerField()
    volunteersRegistered = models.CharField(max_length=80, blank=True)
    description = models.TextField(blank=True)

    volunteersNeeded.verbose_name = 'Volunteers Needed'
    volunteersRegistered.verbose_name = 'Volunteers Registered'

    class Meta:
        permissions = (
                ('add_chaperones', 'Can sign up chaperones'),
                ('remove_chaperones', 'Can remove chaperones'),
                ('view_chaperones', 'Can view chaperones'),
                ('sign_up', 'Can sign up for an event')
        )

    def __unicode__(self):
        return '%s on %s with %s' % (self.name, self.date.strftime('%c'),
                self.admin)

    def get_absolute_url(self):
        return '/chaperone/eventPage/%d' % self.pk

    @staticmethod
    def future_events(now=datetime.utcnow().replace(tzinfo=utc)):
        ''' Returns a queryset of events that have not happened.

        You can pass in an optional datetime object to over ride
        the comparison date.'''

        return Event.objects.filter(date__gte=now).order_by('date')

    def getPks(self):
        try:
            pks = json.loads(self.volunteersRegistered)
        except ValueError:
            pks = []
        return pks

    def getVolunteers(self):
        '''Returns a list of volunteer User objects.'''

        volunteerPKs = self.getPks()
        if not volunteerPKs:
            return None

        users = []
        for pk in volunteerPKs:
            user = User.objects.get(pk=pk)
            users.append(user)

        return users
    
    def showVolunteerLinks(self):
        pks = self.getPks()
        links = ''
        for pk in pks:
            try:
                user = User.objects.get(pk=pk)
            except:
                pass
            string = '<a href="%s">%s</a>'
            url = user.get_absolute_url()
            username = user.get_full_name() or str(user)
            string = string % (url, username)
            if links == '':
                links += string
            else:
                links += ',' + string
        return links

    def expired(self, now=datetime.utcnow().replace(tzinfo=utc)):
        ''' Returns True if the event has already passed.

        This will be called every time a user opens an event page.
        Implementation of this is method is the only missing piece
        of this functionality.'''

        return self.date < now

    def signedUp(self, user):
        '''Return true if the User is signed up for this event.
        
        Experimental functionality - not tested'''
        pks = self.getPks()
        for pk in pks:
            if user.pk == pk:
                return True

        return False 

    def signUp(self, user):
        volunteerPks = self.getPks()
        username = user.get_full_name() or str(user)
        if user.pk in volunteerPks:
            return 'error', '%s is already signed up' % username
        if volunteerPks:
            volunteerPks.append(user.pk)
            self.volunteersRegistered = json.dumps(volunteerPks)
        else:
            self.volunteersRegistered = json.dumps([user.pk,])
        if self.volunteersNeeded > 0:
            self.volunteersNeeded -= 1
        else:
            return 'error', 'Sorry, no more volunteers needed'

        self.save()
        return 'success', 'Signed up %s' % username

    def removeVolunteer(self, user):
        volunteerPks = self.getPks()
        username = user.get_full_name() or str(user)

        if user.pk not in volunteerPks:
            return 'error', 'Can\'t find "%s": Not Found' % username
        volunteerPks.remove(user.pk)
        self.volunteersRegistered = json.dumps(volunteerPks)
        self.volunteersNeeded += 1
        self.save()
        return 'info', 'Unregistered: %s' % username

    def get_description(self):
        return self.description
