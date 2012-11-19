'''
connection name: Test BBHS
Hostname: 10.10.10.201
Port: 389
No encryption
Bind DN or user: CN=Administrator,CN=Users,DC=testad
Bind password: cookies

Objective:
    Collect username and password from user
    Test authentication via LDAP query (pass | fail)
    if passed:
        stuff
    if not passed:
        stuff

To do:
    Connect our custom LDAP authentication to builtin Django auth app
    Data integrity - keep local database sync'ed with LDAP database
        - Minimal info to sync - maybe only username (would have to be unique)
        - Will probably need to get the user's OU for separation and store it
    Define what data to attempt to collect from LDAP after authentication
        - Email
        - Full name
        - Organizational unit (different user privilidges in Django auth system)
            - Teacher
            - Student
            - Parent
            - School admin
            - Tech admin
    Collect missing data from LDAP search
'''

import ldap

from config import server, port, who, cred
# Basic settings

try:
    l = ldap.open(server, port)
    l.simple_bind_s(who, cred)

    print 'Successfully Authenticated!\n' + '=' * 72 + '\n'
except ldap.LDAPError, e:
    print e

baseDN = 'ou=TA,DC=bbhstech,DC=org'
searchScope = ldap.SCOPE_SUBTREE
retrieveAttributes = None
searchFilter = 'cn=*jose*'

try:
    ldap_result_id = l.search(baseDN, searchScope, searchFilter,
            retrieveAttributes)
    print 'Result id:', ldap_result_id
    result_set = []
    print 'Entering search iteration...'
    while True:
        result_type, result_data = l.result(ldap_result_id, 0) # ?
        print 'Result type:', result_type
        print 'Result data:', result_data
        if result_data == []:
            break
        elif result_type == ldap.RES_SEARCH_ENTRY:
            print 'Result type is %r' % ldap.RES_SEARCH_ENTRY
            result_set.append(result_data)
        print '\n' + '*' * 72

    print '\n\nRESULT SET\n', result_set
except ldap.LDAPError, e:
    print e
