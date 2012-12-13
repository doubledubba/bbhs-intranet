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

    def __unicode__(self):
        return '%s on %s with %s' % (self.name, self.date.strftime('%c'),
                self.admin)

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
        '''Returns a string of volunteers

        The volunteers returned have all signed up for this event.
        NOTICE: The pk of the User and UserProfile MAY NOT BE EQUAL
        Use the User's pk for security.'''

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


        

    def expired(self, now=datetime.utcnow().replace(tzinfo=utc)):
        ''' Returns True if the event has already passed.

        This will be called every time a user opens an event page.
        Implementation of this is method is the only missing piece
        of this functionality.'''

        return self.date < now
