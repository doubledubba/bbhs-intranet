import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from tempfile import NamedTemporaryFile as temp
from ldif import LDIFParser
from django.contrib.auth.models import User
from settings import PROJECT_ROOT, AUTH_LDAP_SERVER_URI
from settings import AUTH_LDAP_BIND_PASSWORD, AUTH_LDAP_BIND_DN, faculty_cn

fh = temp()
command = 'ldapsearch -a always -H %s -w %s -D "%s" -b "%s" "sAMAccountName=*" -u -s sub sAMAccountName > %s'
command = command % (AUTH_LDAP_SERVER_URI, AUTH_LDAP_BIND_PASSWORD, AUTH_LDAP_BIND_DN, faculty_cn, fh.name)
os.system(command)

class MyLDIF(LDIFParser):
    def __init__(self,input):
        LDIFParser.__init__(self,input)
        self.usernames = []

    def handle(self, dn, _entry):
        entry = _entry.get('sAMAccountName')
        if entry:
            self.usernames.append(entry[0])

fh.seek(0)  
parser = MyLDIF(fh)
parser.parse()
print parser.usernames

fh.close()
