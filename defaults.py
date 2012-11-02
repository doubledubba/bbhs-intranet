"Creates default data in the database!"
import os
from datetime import datetime
os.environ['DJANGO_SETTINGS_MODULE'] = 'bbhs.settings'

from django.utils.timezone import utc
from chaperone.models import *

luis = UserProfile.objects.get(user__username='luis')

events = [
        {
            'name': 'Sample event',
            'admin': luis,
            'date': datetime.utcnow().replace(tzinfo=utc),
            'volunteersNeeded': 4,
            'description': 'lada lada lada!'
            }
        ]

for info in events:
    event = Event(**info)
    event.save()
