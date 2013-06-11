from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from markdown import markdown

from chaperone.models import Event, Note
from query import get_query
from datetime import datetime
from urllib import urlencode

'''TODO:
+ Increment/Decrement USER'S eventsNeeeded
+ User Profile pages
+ LDAP Bug
    - Over-riding
    - Updating db
+ Custom links for auth'ed users
+ Setup groups
+ Remove users who are already signed up on the event signup page
+ Automatic Email/Twilio Notifications for users/admins
+ Form for manual notifications
+ Hosting
    - Web Server (Gunicon? Nginx?)
+ Re-structuring code
    - Add eventPK in a field for userProfile in chaperone
+ Add URL Shortener app
+ Collect contact info from users
'''

def notify(alert, message, thanks='/chaperone/'):
    thanks += '?'
    thanks += urlencode({'alert': alert, 'message': message})

    return redirect(thanks)

def formatTAH(TAH):
    string = '['
    for item in TAH:
        string += '"%s",' % item
    string = string[:-1]
    string += ']'
    return string

def getTypeAhead(Model, *attrs):
    names = []
    for model in Model.objects.all():
        for attr in attrs:
            names.append(getattr(model, attr))
    string = formatTAH(names)
    return string

@login_required
def index(request):
    params = {'events': Event.future_events()}
    params['enable_search_bar'] = True
    params['alert'] = request.GET.get('alert')
    params['message'] = request.GET.get('message')
    params['typeAheadSource'] = getTypeAhead(Event, 'name')
    q = request.GET.get('q')
    params['q'] = q
    if q and q.strip():
        start = datetime.now()
        event_query = get_query(q, ['name', 'description'])
        found_entries = Event.objects.filter(event_query).order_by('-date')
        params['events'] = found_entries
        params['latency'] = (datetime.now() - start).total_seconds()
        params['n'] = len(found_entries)
    return render(request, 'chaperone/index.html', params)


@login_required
def eventPage(request, eventID):
    event = get_object_or_404(Event, pk=eventID)
    params = {'event': event}
    params['public_notes'] = Note.objects.filter(event=event,
            public=True).order_by('-pub_date')
    isAdmin = request.user.pk == event.admin.pk
    params['isAdmin'] = isAdmin
    private_notes = Note.objects.filter(event=event, public=False).order_by('-pub_date')
    params['private_notes'] =private_notes if isAdmin else False
    params['alert'] = request.GET.get('alert')
    params['message'] = request.GET.get('message')

    params['view_chaperones'] = request.user.has_perm('chaperone.view_chaperones')
    params['add_chaperones'] = request.user.has_perm('chaperone.add_chaperones')
    params['remove_chaperones'] = request.user.has_perm('chaperone.remove_chaperones')
    params['sign_up'] = request.user.has_perm('chaperone.sign_up')
    params['unsign_up'] = request.user.has_perm('chaperone.unsign_up')

    signUpTAH = []
    for user in User.objects.filter(is_active=True):
        fName = user.get_full_name()
        if fName:
            name = '%s (%s)' % (fName, user.username)
        else:
            name = user.username
        signUpTAH.append(name)
    params['signUpTAH'] = formatTAH(signUpTAH)


    if params['add_chaperones']:
        all_users = User.objects.all()
        users = []
        for user in all_users:
            if str(user.pk) not in event.volunteersRegistered:
                users.append(user)
        params['users'] = users
    params['description'] = markdown(event.description) if event.markdown else event.description

    return render(request, 'chaperone/eventPage.html', params)


def handleRegistration(request, eventID):
    eventID = request.POST.get('q') or eventID
    return HttpResponse(eventID)


def signUp(request, eventID):

    event = get_object_or_404(Event, pk=eventID)
    userPk = request.POST.get('userPk') or str(request.user.pk)
    user = User.objects.get(pk=userPk)
    alert, message = event.signUp(user)

    return notify(alert, message, event.get_absolute_url())

def addNote(request, eventID):
    event = get_object_or_404(Event, pk=eventID)
    userPk = request.POST.get('userPk') or str(request.user.pk)
    user = User.objects.get(pk=userPk)
    text = request.POST.get('note')
    if text:
        private = request.POST.get('private')
        private = True if private else False
        note = Note()
        note.event = event
        note.author = user
        note.text = text
        note.public = not private
        note.save()
        message = 'Note added'
        alert = 'success'
    else:
        alert= 'error'
        message = 'Something went wrong!'
    return notify(alert, message, event.get_absolute_url())

def removeUser(request, eventID):
    event = Event.objects.get(pk=eventID)
    userPk = request.POST.get('userPk')
    if not userPk:
        url = event.get_absolute_url() + '?'
        url += urlencode({'alert': 'error', 'message': 'No users left to remove!'})
        return redirect(url)
    user = User.objects.get(pk=userPk)
    alert, message = event.removeVolunteer(user)
    return notify(alert, message, event.get_absolute_url())
    
