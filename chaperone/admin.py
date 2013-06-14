import os

from markdown import markdown

from django.contrib import admin
from django.template import Context, Template
from chaperone.models import Event, Note
from bbhs.settings import sendHTMLEmail
from chaperone.cron import monthly, daily
from intranet.models import UserProfile

from bbhs.settings import sendHTMLEmail, PROJECT_ROOT

TEMPLATE_DIR = os.path.join(PROJECT_ROOT, 'templates')
TEMPLATE_DIR = os.path.join(TEMPLATE_DIR, 'email')
with open(os.path.join(TEMPLATE_DIR, 'ad.html'), 'r') as fh:
    HTMLTemplate = fh.read()

with open(os.path.join(TEMPLATE_DIR, 'ad.txt'), 'r') as fh:
    TextTemplate = fh.read()

def turnOnRender(modelAdmin, request, querySet):
    querySet.update(markdown=True)

def turnOffRender(modelAdmin, request, querySet):
    querySet.update(markdown=False)

def eventAd(modelAdmin, request, querySet):
    users = UserProfile.objects.filter(eventsNeeded__gt=0,
            user__is_active=True)
    for event in querySet:
        for user in users:
            email = user.user.email
            if not email: continue
            if event.signedUp(user):
                continue
            params = {'user': user, 'event': event}
            params['body'] = markdown(event.description) if event.markdown else event.description

            t = Template(HTMLTemplate)
            c = Context(params)
            html = t.render(c)

            t = Template(TextTemplate)
            c = Context(params)
            text = t.render(c)
            sendHTMLEmail(text, html, 'Chaperone obligation', email)


def eventReminder(modelAdmin, request, querySet):
    for event in querySet:
        for user in event.getVolunteers():
            daily.sendEmail(user, event)


turnOnRender.short_description = 'Turn on the markdown rendering feature'
turnOffRender.short_description = 'Turn off the markdown rendering feature'
eventAd.short_description = 'Event Ad for unregistered users'
eventReminder.short_description = 'Event reminder for registered users'


class EventAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    #exclude = ('volunteersRegistered',)
    list_display = ('name', 'date', 'admin', 'volunteersNeeded', 'showVolunteers', 'markdown')
    list_editable = ['volunteersNeeded',]
    list_filter = ('date', 'admin')
    search_fields = ['name']
    actions = [turnOnRender, turnOffRender]
    actions += [eventAd, eventReminder]

def makePublic(modelAdmin, request, querySet):
    querySet.update(public=True)

def makePrivate(modelAdmin, request, querySet):
    querySet.update(public=False)

makePublic.short_description = 'Make public'
makePrivate.short_description = 'Make private'

class NoteAdmin(admin.ModelAdmin):
    date_hierarchy = 'pub_date'
    list_display = ['getText', 'event', 'author', 'pub_date', 'public']
    actions = [makePublic, makePrivate]

admin.site.register(Event, EventAdmin)
admin.site.register(Note, NoteAdmin)
