from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from chaperone.models import Event

from urllib import urlencode

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
    alert, message = event.signUp(user)
    thanks = '/chaperone/?'
    thanks += urlencode({'alert': alert, 'message': message})

    return redirect(thanks)

def removeUser(request):
    userPk = request.POST.get('userPk')
    if not userPk:
        raise Http404
    user = User.objects.get(pk=userPk)
    return HttpResponse(user)
