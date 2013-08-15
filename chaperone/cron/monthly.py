'''
This cron job will run once a month, and remind users of their yearly chaperone
obligations (4)
'''
import os
import sys
#path = os.path.join(os.environ['HOME'], 'bbhs_intranet')
path = os.path.join('/home/luis', 'bbhs_intranet')
sys.path.append(path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'bbhs.settings'

from django.contrib.auth.models import User
from django.template import Context, Template
from chaperone.models import Event
from bbhs.settings import sendTextEmail, sendHTMLEmail, PROJECT_ROOT

TEMPLATE_DIR = os.path.join(PROJECT_ROOT, 'templates')
TEMPLATE_DIR = os.path.join(TEMPLATE_DIR, 'email')
with open(os.path.join(TEMPLATE_DIR, 'duty.html'), 'r') as fh:
    HTMLTemplate = fh.read()

with open(os.path.join(TEMPLATE_DIR, 'duty.txt'), 'r') as fh:
    TextTemplate = fh.read()

def sendEmail(user):
    email = user.email
    events = Event.future_events().order_by('date')[:5] 
    params = {'user': user, 'events': events}

    t = Template(HTMLTemplate)
    c = Context(params)
    html = t.render(c)

    t = Template(TextTemplate)
    c = Context(params)
    text = t.render(c)

    sendHTMLEmail(text, html, 'Chaperone obligation', email)
#adsfdas

def run():
    for user in User.objects.filter(is_active=True):
        if not user.groups.filter(name='Chaperone_Requirement').exists():
            #print 'Skipping:', user
            continue
        profile = user.get_profile()

        if profile.eventsNeeded > 0:
            if user.email:
                print 'Emailing: %s at %s' % (user.username, user.email)
                sendEmail(user)
            else:
                print '%s has no email!' % user.username
if __name__ == '__main__':
    run()
