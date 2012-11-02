from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.timezone import utc

class UserProfile(models.Model):
    user = models.OneToOneField(User)

    eventsNeeded = models.IntegerField(null=True)

    def __unicode__(self):
        return self.user.username


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


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)

