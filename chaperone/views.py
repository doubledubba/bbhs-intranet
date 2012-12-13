from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from chaperone.models import Event

@login_required
def index(request):
    params = {'events': Event.future_events()}
    return render(request, 'chaperone/index.html', params)


@login_required
def eventPage(request, eventID):
    event = get_object_or_404(Event, pk=eventID)
    params = {'event': event}
    return render(request, 'chaperone/eventPage.html', params)
