import json
from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import utc
from intranet.models import UserProfile

class Event(models.Model):
    name = models.CharField(max_length=80)
    admin = models.ForeignKey(UserProfile)
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

    def showVolunteers(self):
        return '<a href="google.com">asdf</a>'
        pks = self.getPks()
        names = ''
        if pks:
            for pk in pks:
                user = User.objects.get(pk=pk)
                username = user.get_full_name() or str(user)
                if names == '':
                    names = username
                else:
                    names += ', ' + username
            return names

    def expired(self, now=datetime.utcnow().replace(tzinfo=utc)):
        ''' Returns True if the event has already passed.

        This will be called every time a user opens an event page.
        Implementation of this is method is the only missing piece
        of this functionality.'''

        return self.date < now

    def signedUp(self, user):
        '''Return true if the User is signed up for this event.
        
        Experimental functionality - not tested'''

        users = self.volunteers
        return str(user.pk) in self.volunteersRegistered

    def signUp(self, user):
        volunteerPks = self.getPks()
        if user.pk in volunteerPks:
            return 'error', '%s is already signed up' % user
        if volunteerPks:
            volunteerPks.append(user.pk)
            self.volunteersRegistered = json.dumps(volunteerPks)
        else:
            self.volunteersRegistered = json.dumps([user.pk,])

        self.save()
        return 'success', 'Signed up %s' % user

    def removeVolunteer(self, user):
        ''' BUG HUGE BUG
        What about users with PK's larger than one digit?
        '''
        volunteerPks = self.getPks()
        if user.pk not in volunteerPks:
            return 'error', 'Can\'t find "%s": Not Found' % user
        volunteerPks.remove(user.pk)
        self.volunteersRegistered = json.dumps(volunteerPks)
        self.save()
        return 'info', 'Unregistered: %s' % user
