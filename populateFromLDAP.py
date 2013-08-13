import os
from sys import argv, path
path.append('/home/luis/bbhs_intranet')
os.environ['DJANGO_SETTINGS_MODULE'] = 'bbhs.settings'
from tempfile import NamedTemporaryFile as temp
from ldif import LDIFParser
from django.contrib.auth.models import User, Group
from bbhs.settings import PROJECT_ROOT, AUTH_LDAP_SERVER_URI
from bbhs.settings import AUTH_LDAP_BIND_PASSWORD, AUTH_LDAP_BIND_DN, faculty_cn

faculty_cn = 'OU=Faculty,OU=Staff,DC=campus,DC=bishopblanchet,DC=org'
staff_cn = 'OU=Administration,OU=Staff,DC=campus,DC=bishopblanchet,DC=org'

print '1:', faculty_cn
print '2:', staff_cn
print '3: Custom (type in dn)'

response = raw_input('> ')

if response == '1':
    cn = faculty_cn
elif response == '2':
    cn = staff_cn
else:
    cn = response


fh = temp()
command = 'ldapsearch -a always -H %s -w %s -D "%s" -b "%s" "sAMAccountName=*" -u -s sub sAMAccountName mail givenName sn userAccountControl> %s'
command = command % (AUTH_LDAP_SERVER_URI, AUTH_LDAP_BIND_PASSWORD, AUTH_LDAP_BIND_DN, cn, fh.name)
os.system(command)
deList = lambda obj: obj[0] if obj else ''

'''
User Account Control States

66080 --> Password not required | Normal account | Don't expire
66082 --> Account disable | Password not required | Normal account
512 --> Normal Account
66048 --> Normal acccount | Don't expire password
66050 --> Account disable | normal | no expire password
514 --> Account disable | Normal account

Disabled = ['66082', '66050', '514']
'''

class MyLDIF(LDIFParser):
    def __init__(self,input):
        LDIFParser.__init__(self,input)
        self.users = []

    def handle(self, dn, _entry):
        username = _entry.get('sAMAccountName')
        if not username:
            return
        email = _entry.get('mail')
        first_name = _entry.get('givenName')
        last_name = _entry.get('sn')
        UAC = _entry.get('userAccountControl')
        
                
        username = deList(username)
        email = deList(email)
        first_name = deList(first_name)
        last_name = deList(last_name)
        UAC = deList(UAC)
        
        if UAC in ['66082', '66050', '514']:
            print 'Skipping disabled user:', username
            return
        
        user = {'username': username, 'email': email, 
            'first_name': first_name, 'last_name': last_name}
        self.users.append(user)

fh.seek(0)  
parser = MyLDIF(fh)
parser.parse()
users = parser.users
fh.close()
del parser, fh, os, temp, LDIFParser

staff = Group.objects.get(name="Staff")

for user in users:
    print user['username']

#exit(0)


for user in users:
    username = user.get('username')
    email = user.get('email')
    first_name = user.get('first_name')
    last_name = user.get('last_name')
    
    try:
        user = User.objects.get(username=username)
        print username, 'already exists!'
    except User.DoesNotExist:
        user = User()
        user.username = username
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        staff.user_set.add(user)
        print 'Created:', username
    

