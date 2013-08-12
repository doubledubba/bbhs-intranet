Frequently Asked Questions
==========================

Here are some pre-emptively forumulated FAQ's for the admins

A user can't sign in
--------------------

You want to find an old event
-----------------------------

You want to pull up random info
-------------------------------

Say you want some information that isn't visible on the page, but you are
pretty sure is stored in the database somewhere. Give me a call and I can do
some database queries for you.

For example, say you want a list of all the members of group "x", or you want
to see a user's sign up/unsign up history, or you want to see a custom user
report such as how many events does user a have in common with user b. 

Those are just a few of many things that can be quickly computed with django's
database query API in python. Feel free to take a look at the source code to
get a feel for what data is in there and what's not.

https://github.com/luisnaranjo733/bbhs-intranet

The database stuff is in chaperone/models.py or intranet/models.py

If you want to hack at it yourself, here is a sample query:

cd ~/bbhs-intranet
python manage.py shell
from chaperone.models import Event, Note
from intranet.models import UserProfile

a = UserProfile.objects.get(username='cconnors').user
b = UserProfile.objects.get(username='mfreyman').user

matches = []

for event in Event.objects.all():
    volunteers = event.getVolunteers() #this is a list of volunteers
    if a in volunteers and b in volunteers:
        matches.append(event)

print matches

You want to disable the email reminders
---------------------------------------

Just disable the cron jobs:

~/bbhs_intranet/chaperone/cron/daily.py

This job runs once a day, and it checks for events that are happening within
two days.

It sends an email reminder about the event to all of the signed up chaperones.

~/bbhs_intranet/chaperone/cron/daily.py

This runs once a month, and it goes through the users and checks to see if
they've fulfilled their service requirement. If they haven't, then it sends
them an email to remind them to get on it.
