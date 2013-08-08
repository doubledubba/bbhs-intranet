import os
import sys
sys.path.append('/home/luis/bbhs_intranet/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'bbhs.settings'

from bbhs.settings import startOfYear, endOfYear, OBLIGATION_NUMBER
from intranet.models import UserProfile

for profile in UserProfile.objects.all():
    if not profile.user.is_active:
        continue
    if profile.eventsNeeded > 0:
        print '%s is missing %d events' % (profile.user.username,
                profile.eventsNeeded)

# 0 0 1 7 * /path/to/script
# July 1 - deadline for obligation

