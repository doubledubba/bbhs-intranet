BBHS Intranet
=============
Global BBHS intranet

Chaperone
---------
Automatic chaperone sign up system

Service
-------
Service hours collection system

Screencast text walkthrough
---------------------------

Welcome to the intranet!
We can sign in using the school's LDAP authentication system.
it works!
in the future, the website will be able to send emails and/or text messages to communicate with the users.
The idea is that the web service will be able to remind them of their signed up events, and remind them periodically through the year of the remaining events that they need to do.

The web service would know how many events each chaperone needs.
The default is 4, but that can be edited in the database manager.

dkats now needs 80 events.

The web service also has a built-in permission system that can be managed by a priviledged user.

Also, you need to be authenticated in order to view the data. :)

Notice that this user that is logged in cannot see other volunteers, and the "remove other users" tab is not available.

An admin can pick and choose specific permissions for a specific user, or it can place a user into a "group", that propagates shared permissions for all of the group's members.

By default, only the tech office security group members have access to the admin interface.

On the topic of authentication:
Members of the "Staff" security group have bare minimum access for logging in.

When a user logs in, the web service stores that username in a local database, and it pulls metadata like email, full name, etc.. and stores it as well.

The password isn't stored locally, so BBHS LDAP servers (the ones that are used for Moodle) need to be online.

There is a backup authentication backend, that stores local users.
This is a fail-safe. Only the tech office should have access.

Back to the URL shortening system:
It is programmed to not re-add existing urls.
When a link is already stored, it returns the existing one, so there are no duplicates.

In the future, the admin will be able to specify custom url names, like bbhs.org/robotics

For now, the code is generating a unique and random sequence of characters.

That is all!
