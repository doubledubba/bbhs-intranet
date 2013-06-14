'''
This cron job will run once a month, and remind users of their yearly chaperone
obligations (4)
'''
import os
import sys
path = os.path.join(os.environ['HOME'], 'bbhs_intranet')
sys.path.append(path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'bbhs.settings'

from django.contrib.auth.models import User
from django.template import Context, Template
from chaperone.models import Event
from bbhs.settings import sendTextEmail, sendHTMLEmail, PROJECT_ROOT

TEMPLATE_DIR = os.path.join(PROJECT_ROOT, 'templates')
TEMPLATE_DIR = os.path.join(TEMPLATE_DIR, 'email')
with open(os.path.join(TEMPLATE_DIR, 'duty.html'), 'r') as fh:
    template = fh.read()

def sendEmail(user):
    email = user.email
    t = Template(template)
    events = Event.future_events().order_by('date')[:5] 
    params = {'user': user, 'events': events}
    c = Context(params)
    html = t.render(c)
    sendHTMLEmail('Placeholder', html, 'Chaperone obligation', email)
#adsfdas

def run():
    for user in User.objects.filter(is_active=True):
        profile = user.get_profile()
        if profile.eventsNeeded > 0:
            if user.email:
                print 'Emailing:', user.username
                sendEmail(user)
            else:
                print '%s has no email!' % user.username
if __name__ == '__main__':
    run()
