from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
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
    print params, request.user.username
    print request.user.get_all_permissions()
    return render(request, 'chaperone/eventPage.html', params)
