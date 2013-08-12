import re
from datetime import datetime

from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.utils.timezone import utc
from django.contrib.auth.decorators import permission_required

from django.contrib.auth.models import User, Group
from markdown import markdown

from chaperone.models import Event, Note
from query import get_query
from datetime import datetime
from urllib import urlencode

tabs = {
    1: 'active',
    2: '',
    3: ''
}

regex = re.compile(r'\([^)]+\)')
def parseUsername(username):
    r = regex.search(username)
    if r:
        username = r.string[r.start() + 1 : r.end() -1]
        return username
    else:
        return None

def notify(alert, message, thanks='/chaperone/', tab=1):
    thanks += '?'
    thanks += urlencode({'alert': alert, 'message': message, 'tab': tab})

    return redirect(thanks)

def formatTAH(TAH):
    '''Give this a list of strings, and it will spit out a formatted string
    for the typeahead'''

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
            name = getattr(model, attr)
            if name not in names:
                names.append(name)
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
    is_admin = event.admin == request.user
    params['sign_up'] = request.user.has_perm('chaperone.sign_up')
    params['unsign_up'] = request.user.has_perm('chaperone.unsign_up')

    if params['add_chaperones']:
        signUpTAH = []
        for user in User.objects.filter(is_active=True):
            if user == event.admin:
                continue
            fName = user.get_full_name()
            if fName:
                name = '%s (%s)' % (fName, user.username)
            else:
                name = '%s (%s)' % (user.username, user.username)
            signUpTAH.append(name)
        params['signUpTAH'] = formatTAH(signUpTAH)

    if event.markdown:
        description = markdown(event.description)
    else:
        description = '<pre>' + event.description + '</pre>'

    params['description'] = description
    params['markdown'] = event.markdown

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


def handleRegistration(request, eventID):
    if request.method != 'POST':
        raise Http404
    query = request.POST.get('signUpQ')
    r = regex.search(query)
    if r:
        username = r.string[r.start() + 1 : r.end() -1]
        user = get_object_or_404(User, username=username)
        return signUp(request, eventID, user)
    else:
        event = get_object_or_404(Event, pk=eventID)
        params = {
            'tab': '3',
            'message': 'Sorry, "%s" is not a real user!' % query,
            'alert': 'error'
        }
        url = event.get_absolute_url() + '?' + urlencode(params)
        return redirect(url)



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
    
def userReportForm(request):
    params = {}
    if request.method == 'POST':
        params['start'] = request.POST.get('start')
        params['end'] = request.POST.get('end')
        username = request.POST.get('user')
        username = parseUsername(username)
        if not params['start'] and not params['end'] and not username:
            return notify('error', 'You need to fill out the form!',
                    thanks='/chaperone/userReport')

        if not username:
            return notify('error', 'You need to enter a user!',
                    thanks='/chaperone/userReport')
        url = '/chaperone/userReport/%s?' % username
        url += urlencode(params)

        return redirect(url)
    else:
        signUpTAH = []
        for user in User.objects.filter(is_active=True):
            fName = user.get_full_name()
            if fName:
                name = '%s (%s)' % (fName, user.username)
            else:
                name = '%s (%s)' % (user.username, user.username)
            signUpTAH.append(name)
        params = {'TAH': formatTAH(signUpTAH)}
        params['message'] = request.GET.get('message')
        params['alert'] = request.GET.get('alert')
        return render(request, 'chaperone/userReportForm.html', params)

#from django.utils.timezone import utc
#datetime.utcnow().replace(tzinfo=utc)
def userReport(request, username):
    user = get_object_or_404(User, username=username)
    start = request.GET.get('start')
    end = request.GET.get('end')
    try:
        start = datetime.strptime(start, '%m/%d/%Y %X %p')
        end = datetime.strptime(end, '%m/%d/%Y %X %p')
        range = True
    except ValueError:
        range = False
    events = []
    print dir(start), type(start), repr(start)
    for event in Event.objects.all():
        if not event.signedUp(user):
            continue
        if range:
            start = start.replace(tzinfo=utc)
            end = end.replace(tzinfo=utc)
            if start < event.date < end:
                events.append(event)
        else:
            events.append(event)
            start = ''
            end = ''

    count = len(events)
    params = {'user': user, 'events': events,
            'start': start, 'end': end, 'count': count}
    return render(request, 'chaperone/userReport.html', params)


@permission_required('chaperone.create_event')
@login_required
def addEvent(request):
    if request.method == 'POST':
        info = {
            'name': request.POST.get('eventName'),
            'admin': request.POST.get('admin'),
            'volunteersNeeded': request.POST.get('volunteers'),
            'date': request.POST.get('date'),
            'description': request.POST.get('desc'),
            'markdown': request.POST.get('markdown') == 'true' or False,
            'weight': request.POST.get('weight')
        }
        # add GET param UX feedback
        # or re-fill incomplete forms
        try:
            info['date'] = datetime.strptime(info['date'], '%m/%d/%Y %I:%M:%S %p').replace(tzinfo=utc)
        except ValueError:
            return HttpResponse('Invalid format!', content_type='text/plain')

        try:
            info['volunteersNeeded'] = int(info['volunteersNeeded'])
            print 'ined'
        except ValueError:
            return HttpResponse('you need to enter a number for volunteers needed')

        info['admin'] = get_object_or_404(User, pk=info['admin'])
        event = Event(**info)
        event.save()

        i = 1
        dates = []
        for each in range(365): # precautionary infinite recursion prevention
            date = request.POST.get('date' + str(i))
            if date:
                i += 1
                # check for strptime correct format
                try:
                    date = datetime.strptime(date, '%m/%d/%Y %I:%M:%S %p').replace(tzinfo=utc)
                except ValueError:
                    print 'Invalid format!'
                dates.append(date)
            else:
                break
        
        for date in dates:
            info['date'] = date
            event = Event(**info)
            event.save()
        
        url = '/chaperone/eventAdded/?' + urlencode({'i': i})
        return redirect(url)
        return HttpResponse('text', content_type='text/plain')

    event_admins = Group.objects.get(name="Intranet_Event_Admin")
    params = {
        'admins': event_admins.user_set.all()
    }
    return render(request, 'chaperone/addEvent.html', params)

def eventAdded(request):
    message = ''
    i = request.GET.get('i')
    if i:
        i = int(i) if i.isdigit() else None
        if i > 1:
            message = '%d events added!' % i
        else:
            message = '%d event added!' % i
    params = {'alert': 'success', 'message': message}
    return redirect('/chaperone/?' + urlencode(params))
    return render(request, 'chaperone/index.html', params)
