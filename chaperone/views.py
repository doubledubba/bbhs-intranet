from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from chaperone.models import Event

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
'''

def notify(alert, message, thanks='/chaperone/'):
    thanks += '?'
    thanks += urlencode({'alert': alert, 'message': message})

    return redirect(thanks)

@login_required
def index(request):
    params = {'events': Event.future_events()}
    params['alert'] = request.GET.get('alert')
    params['message'] = request.GET.get('message')
    return render(request, 'chaperone/index.html', params)


@login_required
def eventPage(request, eventID):
    event = get_object_or_404(Event, pk=eventID)
    params = {'event': event}
    params['alert'] = request.GET.get('alert')
    params['message'] = request.GET.get('message')
    params['view_chaperones'] = request.user.has_perm('chaperone.view_chaperones')
    params['add_chaperones'] = request.user.has_perm('chaperone.add_chaperones')
    params['remove_chaperones'] = request.user.has_perm('chaperone.remove_chaperones')
    params['sign_up'] = request.user.has_perm('chaperone.sign_up')
    params['users'] = User.objects.all()
    return render(request, 'chaperone/eventPage.html', params)


def signUp(request, eventID):
    event = get_object_or_404(Event, pk=eventID)
    userPk = request.POST.get('userPk') or str(request.user.pk)
    user = User.objects.get(pk=userPk)
    alert, message = event.signUp(user)
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
    
