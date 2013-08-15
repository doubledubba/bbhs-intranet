import os
import sys
sys.path.append('/home/luis/bbhs_intranet/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'bbhs.settings'

from bbhs.settings import DEADLINE_EMAIL

from bbhs.settings import OBLIGATION_NUMBER, sendHTMLEmail, sendTextEmail
from intranet.models import UserProfile

failures = []

for profile in UserProfile.objects.all():
    if not profile.user.is_active:
        continue
    if profile.eventsNeeded > 0:
        print '%s is missing %d events' % (profile.user.username,
                profile.eventsNeeded)
        failures.append(profile)

txt = '''Hello! This is the chaperone system. I just thought I\'d let you know
which users failed to complete their chaperone requirements, according to my
data:
    
'''

for user in failures:
    txt += '%s is missing %s event units.\n' % (user, user.eventsNeeded)

sendTextEmail(txt, 'Chaperone deadline missers', DEADLINE_EMAIL)



# 0 0 1 7 * /path/to/script
# July 1 - deadline for obligation

