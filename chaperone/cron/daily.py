'''
This cron job will run once a day, and remind users of their upcoming chaperone
obligations (4)
'''
import os
import sys
from datetime import datetime
path = os.path.join(os.environ['HOME'], 'bbhs_intranet')
sys.path.append(path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'bbhs.settings'

from django.utils.timezone import utc
from django.contrib.auth.models import User
from django.template import Context, Template
from chaperone.models import Event
from bbhs.settings import sendTextEmail, sendHTMLEmail, PROJECT_ROOT

TEMPLATE_DIR = os.path.join(PROJECT_ROOT, 'templates')
TEMPLATE_DIR = os.path.join(TEMPLATE_DIR, 'email')
with open(os.path.join(TEMPLATE_DIR, 'eventReminder.html'), 'r') as fh:
    template = fh.read()


for event in Event.future_events():
    now = datetime.utcnow().replace(tzinfo=utc)
    if (event.date - now).days <= 2 and event.volunteersRegistered:
        for user in event.getVolunteers():
            t = Template(template)
            params = {'user': user, 'event': event}
            c = Context(params)
            html = t.render(c)
            #sendHTMLEmail('Placeholder', html, 'Chaperone obligation', user.email)
            print 'Bugging "%s" about "%s"' % (user.username, event.name)

