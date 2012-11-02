from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from chaperone.models import Event, UserProfile

@login_required
def index(request):
    params = {'events': Event.future_events()}
    return render(request, 'chaperone/index.html', params)

def signup(request, eventID):
    event = Event.objects.get(pk=eventID)
    volunteer = request.user.get_profile()
    if event.volunteerRegistered(volunteer):
        return HttpResponse('Youve already registered')
    if event.volunteersNeeded > 0:
        event.addVolunteer(volunteer)
        return HttpResponse('I have registered you!')
    else:
        return HttpResponse('Sorry, we dont need more volunteers')

