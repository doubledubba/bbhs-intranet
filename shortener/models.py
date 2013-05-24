from django.db import models
from django import forms
from bbhs.settings import DOMAIN
maxUrlDisplay = 40


class Url(models.Model):
    long = models.URLField()
    short = models.CharField(max_length=6)

    def __unicode__(self):
        return self.name()
    
    def get_absolute_url(self):
        return 'http://' + DOMAIN + '/' + self.short

    def name(self):
        if len(self.long) > maxUrlDisplay:
            return self.long[:maxUrlDisplay] + '...'
        else:
            return self.long

class UrlForm(forms.Form):
    long = forms.URLField()
