import os
from sys import argv, path
path.append('/home/luis/bbhs_intranet/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'bbhs.settings'

from django_auth_ldap.backend import LDAPBackend

from argparse import ArgumentParser

desc = '''syncLDAP aims to synchronize the LDAP database with the intranet's
local database. This is necessary because sometimes changes are made on the
LDAP directory, but they aren't applied to the web site until the user logs in. 

In order to circumvent that, this script will go through the specified ou
(default is ou=Faculty,ou=Staff,etc...) and sync each user profile that is also
a member of the Staff group IN DJANGO. Keep in mind that any brand new users
won't get be in that group yet and won't be populated, they first need to sign in or be created manually by an admin
before their sync will work'''


parser = ArgumentParser(prog='syncLDAP.py',description=desc)
parser.add_argument('username', help='Username of user you want to sync')
args = parser.parse_args()

LDAPBackend().populate_user(args.username)

