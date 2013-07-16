from urllib import urlencode

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from chaperone.models import Event, Note

from markdown import markdown

Message = lambda request, msg: render(request, 'message.html', {'msg': msg})

def index(request):
    if request.user.is_authenticated():
        profile = request.user.get_absolute_url()
        profile += '?' + urlencode({'home': True})
        response = redirect(profile)
    else:
        response = render(request, 'index.html')
    return response

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)

    
def message(msg, next=None):
    params = {'message': msg, 'alert': 'error', 'next': next}
    return redirect('/login?' + urlencode(params))

def loginView(request):
    redirectUrl = request.GET.get('next') or '/'
    if request.method == 'POST': # If the form has been submitted...
        form = LoginForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(redirectUrl) # Redirect after POST
                else:
                    return message('Your account has been disabled!',
                            redirectUrl)
            else:
                return message('Your username and password were wrong',
                        redirectUrl)

    else:
        form = LoginForm() # An unbound form

    return render(request, 'login.html', {
        'form': form,
        'message': request.GET.get('message'),
        'alert': request.GET.get('alert'),
    })


def logoutView(request):
    logout(request)
    return Message(request, 'Logged out!')

def userPage(request, username):
    params = {}
    user = get_object_or_404(User, username=username)
    events = []
    for event in Event.objects.all():
        pks = event.getPks()
        if user.pk in pks:
            events.append(event)
    expired = []
    active = []
    for event in events:
        if event.expired():
            expired.append(event)
        else:
            active.append(event)
    params['expired'] = expired
    params['active'] = active
    params['user'] = user
    params['home'] = request.GET.get('home')
    return render(request, 'userPage.html', params)


def monthlyCron(request, username):
    user = User.objects.get(username=username)
    events = Event.future_events().order_by('date')[:5]
    return render(request, 'email/duty.html', {'user': user, 'events': events},
            content_type='text/html')

def dailyCron(request, username):
    user = User.objects.get(username=username)
    for event in Event.objects.all():
        if str(user.pk) in event.volunteersRegistered:
            break
    params = {'user': user, 'event': event}
    params['imglink'] = 'http://faculty.bishopblanchet.org/chaperone/eventPage/%d' % event.pk
    return render(request, 'email/eventReminder.html', params,
            content_type='text/html')

def viewPK(request):
    string = ''
    for user in User.objects.all():
        string += user.username + ' ' + str(user.pk)  + ' ' + str(user.get_profile().pk)
        string += '<br />'
    return HttpResponse(string)

def eventAd(request, eventPK):
    event = get_object_or_404(Event, pk=eventPK)
    params = {'user': request.user.get_profile(), 'event': event}
    params['body'] = markdown(event.description) if event.markdown else event.description
    return render(request, 'email/ad.html', params,
            content_type='text/html')

#event = get_object_or_404(Event, pk=1)
#params = {'event': event}

def signedUp_user(request, text=None):
    params['user'] = request.user.get_profile()
    params['admin'] = request.user.get_profile()
    if text:
        return render(request, 'email/signedUp_user.txt', params)
    return render(request, 'email/signedUp_user.html', params)

def signedUp_admin(request, text=None):
    params['user'] = request.user.get_profile()
    params['admin'] = request.user.get_profile()
    params['notes'] = Note.objects.filter(event=params['event'])
    if text:
        return render(request, 'email/signedUp_admin.txt', params)
    return render(request, 'email/signedUp_admin.html', params)
