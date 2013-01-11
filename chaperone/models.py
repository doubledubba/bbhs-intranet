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
    volunteersRegistered = models.CommaSeparatedIntegerField(max_length=80, blank=True)
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

    def addVolunteer(self, volunteer):
        ''' Handles the registering of volunteers

        volunteer is a User object, not a UserProfile'''


        if not self.volunteersRegistered:
            self.volunteersRegistered = volunteer.pk
        else:
            self.volunteersRegistered += ',%d' % volunteer.pk
        self.save()

    def showVolunteers(self):
        '''DEPRECATED: Returns a string of volunteers

        The volunteers returned have all signed up for this event.
        NOTICE: The pk of the User and UserProfile MAY NOT BE EQUAL
        Use the User's pk for security.
        I replaced this with the lower level getVolunteers method.
        I'm not sure if this can be deleted yet.'''

        volunteerPKs = self.volunteersRegistered.split(',')
        if volunteerPKs == [u'']:
            return 'No volunteers!'

        names = ''
        for pk in volunteerPKs:
            user = User.objects.get(pk=pk)
            if names:
                names += ', %s' % user.username
            else:
                names = user.username

        return names

    def getVolunteers(self):
        '''Returns a list of volunteer User objects.'''

        volunteerPKs = self.volunteersRegistered.split(',')
        if volunteerPKs == [u'']:
            return None

        users = []
        for pk in volunteerPKs:
            user = User.objects.get(pk=pk)
            users.append(user)

        return users

    def expired(self, now=datetime.utcnow().replace(tzinfo=utc)):
        ''' Returns True if the event has already passed.

        This will be called every time a user opens an event page.
        Implementation of this is method is the only missing piece
        of this functionality.'''

        return self.date < now


    def signedUp(self, user):
        '''Return true if the User is signed up for this event.
        
        Experimental functionality - not tested'''

        return str(user.pk) in self.volunteersRegistered

    def signUp(self, user):
        if str(user.pk) in self.volunteersRegistered:
            return 'error', 'User is already signed up'
        if self.volunteersRegistered:
            self.volunteersRegistered += ',%s' % user.pk
        else:
            self.volunteersRegistered = user.pk

        self.save()
        return 'success', 'Signed up user'

    def removeVolunteer(self, user):
        ''' BUG HUGE BUG
        What about users with PK's larger than one digit?
        '''

        if str(user.pk) not in self.volunteersRegistered:
            return 'error', 'Can\'t find "%s": Not Found' % user
        i = self.volunteersRegistered.find(str(user.pk))
        if i == 0:
            self.volunteersRegistered = self.volunteersRegistered[2:]
        else:
            del self.volunteersRegistered[i] # PK
            del self.volunteersRegistered[i] # Comma after PK
        self.save()
        return 'info', 'Unregistered: %s' % user
