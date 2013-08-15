import os
from sys import argv, path
path.append('/home/luis/bbhs_intranet')
os.environ['DJANGO_SETTINGS_MODULE'] = 'bbhs.settings'
from tempfile import NamedTemporaryFile as temp
from ldif import LDIFParser
from django.contrib.auth.models import User, Group
from bbhs.settings import PROJECT_ROOT, AUTH_LDAP_SERVER_URI
from bbhs.settings import AUTH_LDAP_BIND_PASSWORD, AUTH_LDAP_BIND_DN, faculty_cn
from django_auth_ldap.backend import LDAPBackend

BASE_CN = 'OU=Intranet,OU=Technology,OU=Staff,DC=campus,DC=bishopblanchet,DC=org'

Chaperone_Requirement = 'CN=Chaperone_Requirement,' + BASE_CN
Chaperone_Event_Manager = 'CN=Chaperone_Event_Manager,' + BASE_CN
Chaperone_Site_Admin = 'CN=Chaperone_Site_Admin,' + BASE_CN
Intranet_Super_Admin = 'CN=Intranet_Super_Admin,' + BASE_CN
Intranet_Admin_Access = 'CN=Intranet_Admin_Access,' + BASE_CN
Everyone = 'DC=campus,DC=bishopblanchet,DC=org'
Staff = 'OU=Staff,' + Everyone

DNs = {
        1: Chaperone_Requirement,
        2: Chaperone_Event_Manager,
        3: Chaperone_Site_Admin,
        4: Intranet_Super_Admin,
        5: Intranet_Admin_Access,
        6: Everyone,
        7: Staff,
}

print '''PS: For some reason, the active directory doesn\'t show changes until about
30 seconds after the changes were applied. Make sure the sync works, and if it
doesn't, then wait for a bit and try again.

Select a security group or organizationl unit for me to sync
'''

print '1:', Chaperone_Requirement
print '2:', Chaperone_Event_Manager
print '3:', Chaperone_Site_Admin
print '4:', Intranet_Super_Admin
print '5:', Intranet_Admin_Access
print '6:', Staff
print '6:', Everyone
print '7:', Staff

def getResponse():
    try:
        while True:
            response = raw_input('> ')
            if response == '1':
                return 1
            elif response == '2':
                return 2
            elif response == '3':
                return 3
            elif response == '4':
                return 4
            elif response == '5':
                return 5
            elif response == '6':
                return 6
            elif response == '7':
                return 7
    except KeyboardInterrupt:
        print 'You didn\'t select a DN for me to sync!'
        exit(1)

if len(argv) == 1:
    response = getResponse()
else:
    response = int(argv[1])
cn = DNs[response]



fh = temp()
command = 'ldapsearch -a always -H %s -w %s -D "%s" -b "%s" "objectClass=*" -u -s sub member > %s'
command = command % (AUTH_LDAP_SERVER_URI, AUTH_LDAP_BIND_PASSWORD, AUTH_LDAP_BIND_DN, cn, fh.name)
os.system(command)
deList = lambda obj: obj[0] if obj else ''


class MyLDIF(LDIFParser):
    def __init__(self,input):
        LDIFParser.__init__(self,input)
        self.users = []

    def handle(self, dn, _entry):
        member = _entry.get('member')
        if member:
            for dn in member:
                self.users.append(dn)

fh.seek(0)  
parser = MyLDIF(fh)
parser.parse()
users = parser.users
fh.close()
del parser, fh

#---------------------------------------------------------


class Parser(LDIFParser):
    def __init__(self,input):
        LDIFParser.__init__(self,input)
        self.username = ''

    def handle(self, dn, _entry):
        username = _entry.get('sAMAccountName')
        username = deList(username)
        if username:
            
            self.username = username

command = 'ldapsearch -a always -H %s -w %s -D "%s" -b "%s" "objectClass=*" -u -s sub sAMAccountName> %s'

usernames = []
for cn in users:
    fh = temp()
    args = (AUTH_LDAP_SERVER_URI, AUTH_LDAP_BIND_PASSWORD, AUTH_LDAP_BIND_DN, cn, fh.name)
    cmd = command % args
    os.system(cmd)

    parser = Parser(fh)
    parser.parse()
    usernames.append(parser.username)

    fh.seek(0)
    fh.close()

print '\nAbout to sync every user in the "%s" security group.' % cn
print 'USERS'
print '=' * 72
for user in usernames:
    print ' * ' + user

if not len(argv) > 1:
    try:
        raw_input("Hit ENTER to contine.")
    except KeyboardInterrupt:
        exit(1)

for username in usernames:
    LDAPBackend().populate_user(username)

from pprint import pprint

print '\nSynced the following users:'
pprint(usernames)
