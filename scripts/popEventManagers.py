import os
from sys import argv, path
path.append('/home/luis/bbhs_intranet')
os.environ['DJANGO_SETTINGS_MODULE'] = 'bbhs.settings'
from tempfile import NamedTemporaryFile as temp
from ldif import LDIFParser
from django.contrib.auth.models import User, Group
from bbhs.settings import PROJECT_ROOT, AUTH_LDAP_SERVER_URI
from bbhs.settings import AUTH_LDAP_BIND_PASSWORD, AUTH_LDAP_BIND_DN, faculty_cn

cn = 'OU=Administration,OU=Staff,DC=campus,DC=bishopblanchet,DC=org'
cn = 'CN=Intranet_Super_Admin,OU=Intranet,OU=Technology,OU=Staff,DC=campus,DC=bishopblanchet,DC=org'

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

print usernames
