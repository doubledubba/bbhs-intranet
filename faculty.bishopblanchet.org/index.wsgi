import os
import sys
import site

site.addsitedir('/home/luis/.virtualenvs/intranet/local/lib/python2.7/site-packages')

sys.path.append('/home/luis/bbhs_intranet')
sys.path.append('/home/luis/bbhs_intranet/bbhs')

os.environ['DJANGO_SETTINGS_MODULE'] = 'bbhs.settings'

activate_env = os.path.expanduser("/home/luis/.virtualenvs/intranet/bin/activate_this.py")
execfile(activate_env, dict(__file__=activate_env))

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

