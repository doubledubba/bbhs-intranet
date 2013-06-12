from django.contrib import admin
from chaperone.models import Event, Note
from bbhs.settings import sendHTMLEmail
from chaperone.cron import monthly, daily

def turnOnRender(modelAdmin, request, querySet):
    querySet.update(markdown=True)

def turnOffRender(modelAdmin, request, querySet):
    querySet.update(markdown=False)

def eventAd(modelAdmin, request, querySet):
    print 'ad!'

def eventReminder(modelAdmin, request, querySet):
    print 'Reminder!'
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
