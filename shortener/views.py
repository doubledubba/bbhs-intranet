import random
import string

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, render, get_object_or_404

from shortener.models import Url, UrlForm

chars = string.lowercase + string.uppercase + '0123456789'
randomString = lambda: ''.join([random.choice(chars) for a in range(6)])


def index(request):
    if request.method == 'POST':
        form = UrlForm(request.POST)
        if form.is_valid():
            longUrl = form.cleaned_data['long']
            url, created = Url.objects.get_or_create(long=longUrl)
            if created:
                url.short = randomString()
                url.save()
            
            return HttpResponseRedirect('/thanks/%s' % url.short)

    else:
        form = UrlForm()

    return render(request, 'submit.html', {'form': form})


def thanks(request, short):
    url = get_object_or_404(Url, short=short)
    return render(request, 'thanks.html', dict(url=url))


def activate(request, short):
    url = get_object_or_404(Url, short=short)
    return HttpResponseRedirect(url.long)


