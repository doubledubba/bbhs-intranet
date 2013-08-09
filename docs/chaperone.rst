Chaperone App
=============

The chaperone app was created to replace an existing system for managing school
events and their volunteers.

Event listings page and Event pages
--------------------------

There is an event listings page that lists all of the future events in order of
which one is most close to taking place. Users can click on an event and
be taken to that event's corresponding page.

There, users will be able to see
things like the event's date, time, description, administrator, administrator
contact information, notes from the administrator or from other volunteers, a
list of other volunteers, contact info of other volunteers, and how many
volunteers are still needed.

Additionally, users can sign up or unsign up for that particular event on that
page.

Types of users in the chaperone app
-----------------------------------

There are 2 main types of regular users in this app:
    * Event Administrators
    * Chaperones

Site Administrators
*******************

Group doc

Event Administrators
********************

Each event has a single **event administrator**, that is set initially by the site
administrator that created the event. This can be changed by a site admin
later.

There is a restricted group of users who are allowed to be event administrators.

Any site administrator can add or remove users from this group.

**This is a Django group, and it is called "Event Admins". If the database is
every reset, this group needs to be re-created manually through the admin page
verbatim or else the "Add a new event" page will not work**

The event admin's contact info will be posted on the event's description page,
as well as a list of all of the other users who have signed up for the event.
This is safe, because only logged-in users can see this information.

Event administrators can
  * Send emails to the whole BBHS faculty to request volunteers (through a site
    admin)
  * Send email reminders to the event's signed up users (through a site admin)
  * Read the public notes and the private notes that users post on the event's
    page
  * Sign up other users directly for the event
  * Remove other volunteers from the event's registration

Regular users
*************

Most users in the system will be placed here. The regular user will be able to
view all future events, and will be able to sign up or unsign up for events.

Every time a user signs up for an event, his or her required chaperone event
count will be decreased by 1. Likewise, when a user unsigns up, the count will
increment by 1.

If a user goes past his or her requirement count, it will appear as if the user
has reached a plateau of 0 required events, but the application is secretly
going into negative numbers in case that data is ever requested.

Additionally, every time a user signs up for or unsigns up for an event, the
action is logged in the database.

Emails/Cron jobs
----------------

Groups
------

Staff
Event Admins
