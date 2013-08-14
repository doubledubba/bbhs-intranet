import os
from sys import argv, path
path.append('/home/luis/bbhs_intranet')
os.environ['DJANGO_SETTINGS_MODULE'] = 'bbhs.settings'
from django.contrib.auth.models import User, Group, Permission

groups = {
    'Chaperone_Requirement': None,
    'Chaperone_Site_Admin': ['add_chaperones', 'remove_chaperones',
        'view_chaperones', 'sign_up', 'unsign_up', 'create_event',
        'pull_user_reports'],
    'Intranet_Admin_Access': None,
    'Chaperone_Event_Manager': None,
    'Intranet_Super_Admin': None
}

for groupName in groups:
    try:
        group = Group.objects.get(name=groupName)
    except Group.DoesNotExist:
        print groupName, 'didn\'t exist so I created it.'
        group = Group()
        group.name = groupName
        group.save()

    permissions = groups[groupName]
    if permissions:
        for permName in permissions:
            perm = Permission.objects.get(codename=permName)
            group.permissions.add(perm)
            group.save()
