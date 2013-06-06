"Creates default data in the database!"
import os
from datetime import datetime
os.environ['DJANGO_SETTINGS_MODULE'] = 'bbhs.settings'
from urllib2 import urlopen

from django.utils.timezone import utc
from django.contrib.auth.models import User
from chaperone.models import *

fh = urlopen('http://daringfireball.net/projects/markdown/basics.text')
md = fh.read()
fh.close()

luis = User.objects.get(username='luis')

events = [
        {
            'name': 'Sample event',
            'admin': luis,
            'date': datetime.utcnow().replace(tzinfo=utc),
            'volunteersNeeded': 4,
            'description': md
            }
        ]

for info in events:
    event = Event(**info)
    event.save()
    print 'Created the "%s" event for luis.' % info['name']
