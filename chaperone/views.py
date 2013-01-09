from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from chaperone.models import Event


@login_required
def index(request):
    params = {'events': Event.future_events()}
    return render(request, 'chaperone/index.html', params)


@login_required
def eventPage(request, eventID):
    event = get_object_or_404(Event, pk=eventID)
    params = {'event': event}
    params['view_chaperones'] = request.user.has_perm('chaperone.view_chaperones')
    params['add_chaperones'] = request.user.has_perm('chaperone.add_chaperones')
    params['remove_chaperones'] = request.user.has_perm('chaperone.remove_chaperones')
    params['sign_up'] = request.user.has_perm('chaperone.sign_up')
    params['users'] = User.objects.all() # TODO: filter for sign_up perm
    return render(request, 'chaperone/eventPage.html', params)


def signUp(request, eventID):
    event = get_object_or_404(Event, pk=eventID)
    userPk = request.POST.get('userPk') or str(request.user.pk)
    user = User.objects.get(pk=userPk)
    message = event.signUp(user)
    return redirect(event.get_absolute_url())

def removeChaperone(request, eventID):
    event = get_object_or_404(Event, pk=eventID)
    userPk = request.POST.get('userPk') or str(request.user.pk) # local user is
    # being set always BUG
    message = event.removeUser(userPk)
    return redirect(event)
    return HttpResponse(message)

def userPage(request, username):
    return HttpResponse(username)

'''TODO:
    Redirect after forms with status message
    LDAP mirroring bug? *
    Polish gui
    Edge case testing
    Userprofile vs User in models *
    Userprofile initiation requirement in gui *
    Default chaperone events needed for users *
    deployment
    User page w/ require permission to view + populate with relevant data -
'''
