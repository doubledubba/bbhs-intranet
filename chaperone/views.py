import re

from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

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
tabs = {
    1: 'active',
    2: '',
    3: ''
}

def notify(alert, message, thanks='/chaperone/', tab=1):
    thanks += '?'
    thanks += urlencode({'alert': alert, 'message': message, 'tab': tab})

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
    tabs = {
        1: 'active',
        2: '',
        3: ''
    }
    params = {'events': Event.future_events()}
    params['enable_search_bar'] = True
    params['alert'] = request.GET.get('alert')
    params['message'] = request.GET.get('message')
    params['typeAheadSource'] = getTypeAhead(Event, 'name')
    q = request.GET.get('q')
    params['q'] = q
    params['chaperone_page'] = True
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

    if params['add_chaperones']:
        signUpTAH = []
        for user in User.objects.filter(is_active=True):
            fName = user.get_full_name()
            if fName:
                name = '%s (%s)' % (fName, user.username)
            else:
                name = '%s (%s)' % (user.username, user.username)
            signUpTAH.append(name)
        params['signUpTAH'] = formatTAH(signUpTAH)


    params['description'] = markdown(event.description) if event.markdown else event.description

    for i in tabs:
        tabs[i] = ''
    tab = request.GET.get('tab')
    if tab:
        tab = int(tab)
        tabs[tab] = 'active'
    else:
        tabs[1] = 'active'
    params['tab1'] = tabs[1]
    params['tab2'] = tabs[2]
    params['tab3'] = tabs[3]

    return render(request, 'chaperone/eventPage.html', params)

regex = re.compile(r'\([^)]+\)')

def handleRegistration(request, eventID):
    if request.method != 'POST':
        raise Http404
    query = request.POST.get('signUpQ')
    r = regex.search(query)
    username = r.string[r.start() + 1 : r.end() -1]
    user = User.objects.get(username=username)
    return signUp(request, eventID, user)



def signUp(request, eventID, _user=None):

    event = get_object_or_404(Event, pk=eventID)
    userPk = request.POST.get('userPk') or str(request.user.pk)
    user = _user or User.objects.get(pk=userPk)
    alert, message = event.signUp(user)

    return notify(alert, message, event.get_absolute_url(), tab=3)

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
        message = 'Private note added' if private else 'Public note added'
        alert = 'success'
    else:
        alert= 'error'
        message = 'Something went wrong!'
    return notify(alert, message, event.get_absolute_url(), tab=2)

def removeUser(request, eventID):
    event = Event.objects.get(pk=eventID)
    userPk = request.POST.get('userPk')
    if not userPk:
        url = event.get_absolute_url() + '?'
        url += urlencode({'alert': 'error', 'message': 'No users left to remove!'})
        return redirect(url)
    user = User.objects.get(pk=userPk)
    alert, message = event.removeVolunteer(user)
    return notify(alert, message, event.get_absolute_url(), tab=3)
    

def userReport(request, username=''):
    if username:
        user = get_object_or_404(User, username=username)
        return HttpResponse(user)
    else:
        return HttpResponse('adsf')

def addEvent(request):
    params = {
        'admins': User.objects.filter(userprofile__canAdminEvents=True)
    }
    return render(request, 'chaperone/addEvent.html', params)
