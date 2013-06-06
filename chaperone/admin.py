from django.contrib import admin
from chaperone.models import Event

def turnOnRender(modelAdmin, request, querySet):
    querySet.update(markdown=True)

def turnOffRender(modelAdmin, request, querySet):
    querySet.update(markdown=False)

turnOnRender.short_description = 'Turn on the markdown rendering feature'
turnOffRender.short_description = 'Turn off the markdown rendering feature'

class EventAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
 #   exclude = ('volunteersRegistered',)
    list_display = ('name', 'date', 'admin', 'volunteersNeeded', 'showVolunteers', 'markdown')
    list_editable = ['volunteersNeeded',]
    list_filter = ('date', 'admin')
    search_fields = ['name']
    actions = [turnOnRender, turnOffRender]

admin.site.register(Event, EventAdmin)

