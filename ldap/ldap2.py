import ldap

from config import server, port, who, cred
# Basic settings

con = ldap.initialize('ldap://%s' % server)

try:
    con.simple_bind_s(who, cred)
except ldap.INVALID_CREDENTIALS, e:
    print 'Your credentials are invalid!'
except ldap.LDAPError, e:
    print e


