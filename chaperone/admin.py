from django.contrib import admin
from chaperone.models import Event, Note

def turnOnRender(modelAdmin, request, querySet):
    querySet.update(markdown=True)

def turnOffRender(modelAdmin, request, querySet):
    querySet.update(markdown=False)

turnOnRender.short_description = 'Turn on the markdown rendering feature'
turnOffRender.short_description = 'Turn off the markdown rendering feature'

class EventAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    exclude = ('volunteersRegistered',)
    list_display = ('name', 'date', 'admin', 'volunteersNeeded', 'showVolunteers', 'markdown')
    list_editable = ['volunteersNeeded',]
    list_filter = ('date', 'admin')
    search_fields = ['name']
    actions = [turnOnRender, turnOffRender]

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
