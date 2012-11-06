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
        return Event.objects.filter(date__gte=now).order_by('date')

    def addVolunteer(self, volunteer):
        if not self.volunteersRegistered:
            self.volunteersRegistered = volunteer.pk
        else:
            self.volunteersRegistered += ',%d' % volunteer.pk
        self.save()
        print 'Added:', volunteer



