import os
from sys import argv, path
path.append('/home/luis/bbhs_intranet')
os.environ['DJANGO_SETTINGS_MODULE'] = 'bbhs.settings'
from django.contrib.auth.models import User, Group
from chaperone.models import Event, Note

def delete(Model):
    for model in Model.objects.all():
        model.delete()

delete = lambda Model: [model.delete() for model in Model.objects.all()]

if len(argv) > 1 and argv[1].isdigit():
    response = int(argv[1])
else:
    print '1: Groups'
    print '2: Users'
    print '3: Events'
    print '4: Note'
    print '5: All'
    response = raw_input('> ')
    if response.isdigit():
        response = int(response)
    else:
        print 'You need to enter a digit!'
        exit(1)

if response == 1:
    print 'Deleting all Groups...'
    delete(Group)
elif response == 2:
    print 'Deleting all Users...'
    delete(User)
elif response == 3:
    print 'Deleting all Events...'
    delete(Event)
elif response == 4:
    print 'Deleting all Notes...'
    delete(Note)
elif response == 5:
    print 'Deleting all Groups...'
    print 'Deleting all Users...'
    print 'Deleting all Events...'
    print 'Deleting all Notes...'
    delete(Group)
    delete(User)
    delete(Event)
    delete(Note)
else:
    print 'Try again!'
    exit(1)
