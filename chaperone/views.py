from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from chaperone.models import Event, UserProfile

@login_required
def index(request):
    params = {'events': Event.future_events()}
    return render(request, 'chaperone/index.html', params)


