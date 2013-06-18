'''
This cron job will run once a day, and remind users of their upcoming chaperone
obligations (4)
'''
import os
import sys
from datetime import datetime
path = os.path.join('/home/luis', 'bbhs_intranet')
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
    HTMLTemplate = fh.read()

with open(os.path.join(TEMPLATE_DIR, 'eventReminder.txt'), 'r') as fh:
    TextTemplate = fh.read()

def sendEmail(user, event):
    params = {'user': user, 'event': event}

    t = Template(HTMLTemplate)
    c = Context(params)
    html = t.render(c)

    t = Template(TextTemplate)
    c = Context(params)
    text = t.render(c)

    subject = 'Reminder about "%s"' % event.name.capitalize()
    sendHTMLEmail(text, html, subject, user.email)
    print 'Bugging "%s" about "%s"' % (user.username, event.name)

def run():
    for event in Event.future_events():
        now = datetime.utcnow().replace(tzinfo=utc)
        if (event.date - now).days <= 2:
            volunteers = event.getVolunteers()
            if not volunteers:
                print 'No volunteers for ' + str(event)
                continue
            for user in volunteers:
                sendEmail(user, event)



if __name__ == '__main__':
    run()
