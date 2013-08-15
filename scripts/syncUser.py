import os
from sys import argv, path
path.append('/home/luis/bbhs_intranet/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'bbhs.settings'

from django_auth_ldap.backend import LDAPBackend

from argparse import ArgumentParser

desc = '''Use syncUser to sync a single user's information from the active
directory to the Intranet's local database.

This is useful for when you make a change that needs to be immediately take
effect. Without a manual sync such as this one, the change on the directory
won't take place on the site until the user next logs in.'''


parser = ArgumentParser(prog='syncLDAP.py',description=desc)
parser.add_argument('username', help='Username of user you want to sync')
args = parser.parse_args()

LDAPBackend().populate_user(args.username)

