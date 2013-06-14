import json
from datetime import datetime

from markdown import markdown

from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import utc
from intranet.models import UserProfile


class Event(models.Model):
    name = models.CharField(max_length=80)
    admin = models.ForeignKey(User)
    date = models.DateTimeField()
    pub_date = models.DateTimeField(auto_now_add=True)
    volunteersNeeded = models.IntegerField()
    volunteersRegistered = models.CharField(max_length=80, blank=True)
    description = models.TextField(blank=True)
    markdown = models.BooleanField(default=True)
    markdown.allow_tags = True

    volunteersNeeded.verbose_name = 'Volunteers Needed'
    volunteersRegistered.verbose_name = 'Volunteers Registered'

    class Meta:
        permissions = (
                ('add_chaperones', 'Can sign up other chaperones'),
                ('remove_chaperones', 'Can remove other chaperones'),
                ('view_chaperones', 'Can view other chaperones'),
                ('sign_up', 'Can sign up self from an event'),
                ('unsign_up', 'Can unsign up self from an event')
        )

    def __unicode__(self):
        return '"%s" on %s with %s' % (self.name, self.date,
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
            if user.is_active:
                users.append(user)

        return users
 
    def showVolunteers(self):
        volunteers = self.getVolunteers()
        if volunteers:
            return ', '.join([user.get_full_name() or str(user) for user in volunteers])
        else:
            return ''
    showVolunteers.short_description = 'Volunteers'

   
    def showVolunteerLinks(self):
        pks = self.getPks()
        links = ''
        for pk in pks:
            try:
                user = User.objects.get(pk=pk)
                string = '<a href="%s">%s</a>'
                url = user.get_absolute_url()
                username = user.get_full_name() or str(user)
                string = string % (url, username)
                if links == '':
                    links += string
                else:
                    links += ',' + string
            except ValueError: pass
        return links

    def expired(self, now=datetime.utcnow().replace(tzinfo=utc)):
        ''' Returns True if the event has already passed.

        This will be called every time a user opens an event page.
        Implementation of this is method is the only missing piece
        of this functionality.'''

        return self.date < now

    def signedUp(self, user):
        '''Return true if the User is signed up for this event.
        '''
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
        if not self.expired(): # so users dont cheat and sign up for past events
            profile = user.get_profile()
            if profile.eventsNeeded > 0:
                profile.eventsNeeded -= 1
            profile.eventsDone += 1
            profile.save()
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
        if not self.expired():
            profile = user.get_profile()
            profile.eventsNeeded += 1
            profile.eventsDone -= 1
            profile.save()
        return 'info', 'Unregistered: %s' % username

    def get_description(self):
        text = self.description
        limit = 150
        if len(text) > limit:
            text = text[:limit] + '... (more on event page)'
        return text



class Note(models.Model):
    event = models.ForeignKey(Event)
    author = models.ForeignKey(User)
    text = models.TextField("Note text")
    public = models.BooleanField(default=True)
    pub_date = models.DateTimeField("Creation date", auto_now_add=True)

    def __unicode__(self):
        return '<Note #%d event#%d private=%s' % (self.pk,self.event.pk, not
                self.public)

    def getText(self):
        length = len(self.text)
        return self.text if length < 80 else self.text[:80] + '...'
    getText.short_description = 'Note content'


from django.db.models.signals import pre_delete

def delete_user_profile(sender, instance, using, **kwargs):
    print "Deleting", instance
    for event in Event.objects.all():
        event.removeVolunteer(instance)

pre_delete.connect(delete_user_profile, sender=User)
