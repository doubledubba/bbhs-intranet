What to do if:
==============

Here are some pre-emptively forumulated FAQ's for the admins

A user can't sign in
--------------------

Check that they are in the Staff security group
Check that their account hasn't been disabled by an admin

You want to find an old event
-----------------------------

Go in the admin page and look for them there

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

You need to migrate the site
----------------------------

It's a pain in the ass and I don't advise it.

sudo apt-get install git
git clone https://github.com/luisnaranjo733/bbhs-intranet //will download code

sudo apt-get install python-pip // installing dependencies for python2.7
sudo pip install -r requirements.txt

You need to set up a dedicated python production server. I used mod_wsgi for apache.
There are nginx options and several other python specific servers.

sudo mv ~/bbhs-intranet/faculty.bishopblanchet.org /var/www/faculty.bishopblanchet.org
you may have permission issues with this - fix with chmod

You need to reset the database
-------------------------------

cd ~/bbhs-intranet
sudo sh reset_db.sh
// log in with someone who is a member of the "Staff" security group or
// manually create a group named "Staff" in the admin page
python populateFromLDAP.py // this will populate everyone in ou=Faculty
python populateFromLDAP.py staff // this will populate everyone in ou=Administration

You want to change the default event requirement number
-------------------------------------------------------

edit ~/bbhs_intranet/bbhs/settings.py

Change OBLIGATION_NUMBER = 4
Go to the admin page, then go to Users
Select the admin action "Normalize Yearly Obligation" and select everyone

This will reset every active user's events done count for this year, and their events
needed count for this year.

You want to delete a user
-------------------------

You should probably just disable them.
Go to the admin page and click disable and them save.

I coded it so that disabled users don't get to do anything.

You want to send an email advertisement for an event
----------------------------------------------------

asdf

You want to change the year end and year start reset dates
----------------------------------------------------------

Edit the very bottom of the settings file

You want to change LDAP settings
--------------------------------

Just modify the settings.py file. It's pretty straightforward, but let me know
if you need any help. All relevant LDAP related variables are prefixed with
AUTH_LDAP_*

Make sure to restart the apache server for changes to take effect

You messed up/deleted the code
------------------------------

cd ~/bbhs_intranet/
git checkout -- .

This will reset all the code in this directory to the state I left it in last.

This will not change /var/www/faculty.bishopblanchet.org, so I recommend not
touching that folder

In case you deleted ~/bbhs_intranet or ~/bbhs-intranet/.git

git clone https://github.com/luisnaranjo733/bbhs-intranet ~/bbhs_intranet

You want to modify or change HTML
---------------------------------

The html templates are located in ~/bbhs_intranet/bbhs/templates

You can safely make changes, but make sure you don't delete anything that looks
like:

{% stuff %} // template engine constructs, for loops, block tags, etc..
or 
{{ stuff }} variables

If you want to get fancy look up Django's templating system. It's not hard to
learn.

You could take a look at chaperone/views.py or intranet/views.py file for
figuring out what objects and lists are being passed to the templates before
they are rendered in static html

You want to add static files
----------------------------


