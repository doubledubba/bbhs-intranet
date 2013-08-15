What is it?
=======================================

The intranet is an internal web service designed for use by the Bishop Blanchet Staff.

Any BBHS faculty member or BBHS school administrator can log in and use the
site with their existing school username and password.

The idea is that within the intranet, there are several "apps" that can be used
by staff members. Right now, we only have a chaperone app, but we are
looking at expanding the intranet with more apps in the future.

LDAP Authentication
===================

The intranet makes extensive use of the BBHS Active Directory for user
authentication.

It's important to note that the user that is being used by the site for binding
is:

'CN=Luis Naranjo,OU=Technology,OU=Staff,DC=campus,DC=bishopblanchet,DC=org'

and the password is a certain type of baked goods that happened to be the
default password in the first Tech Apprentice class.

So don't move that user, change his password, or change his permissions unless
you change them in the code too.

If you do change them in the code, you would have to modify the
~/bbhs_intranet/bbhs/settings.py file.

Make sure you restart the apache2 service.

Types of users
==============

There are two main types of users in the intranet.

Every user is either a super user, or a regular user.

All super users have the same full permissions, but not all regular users get
the same permissions. That depends on which user-specific permissions they have
been explicitly granted, or which permission groups they belong to.

Super user
----------

A super user has full permissions to access the admin page, and they can add,
remove, or modify any object in the database.

Additionally, a super user has full permissions to do any app-specific actions.

Regular user
------------

Globally, a regular user only has permission to login to the intranet with
their LDAP credentials. The only people who can login are those that are
included in the Staff security group.

A regular user may have further bare-minimum permissions that are specific to
the apps of the intranet.

Permissions
===========

By default, Django comes bundles with a bunch of different permissions that
users and groups can receive (if a user is a member of a group, that user gets
all of the group's permissions added to his/her own).

These permissions are all related to editing, adding, and deleting objects in
the database through the admin page.

They look like this:

admin | log entry | can add log entry
admin | log entry | can change log entry
admin | log entry | can delete log entry

In addition to these standard permissions, I've added permissions that are
specific to each application.

Here are the relevant permissions for the chaperone app:

Can sign up other chaperones
-----------------------------

This allows users to sign up other users at an event's page.

This should not be given to the regular user. Maybe no one should be able to do
this except the superusers who have this permission implicitly.

Can remove other chaperones
---------------------------

This allows users to unsign up other users at an event's page.

Can view other chaperones
-------------------------

This permissions allows users to see what other users have signed up for an
event.

By default, everyone can see how many volunteers are still needed, but to see
who is signed up you need this.

Can sign up self from an event
------------------------------

Every regular user should have this. Without this, they can't sign up for
events

Can unsign up self from an event
--------------------------------

Without this, they can't unsign up for events

Can create events
-----------------

Give this to whoever might be creating events.

This allows them to access the /addEvent page

Pull user reports
-----------------

This permission allows users users to pull user reports on other users in the
chaperone app


Groups
======

The system is set up to be flexible and easily customizable.
The site primarily uses groups to handle user's permissions. I tried to set it
up so the group changes are primarily changed in the existing LDAP
database.

In addition to using groups to handle user's permissions, individual user
permissions can be modified at will in the admin page with the same effect. 

It's important to note that the site will mirror all of the user's LDAP groups
over to Django if the groups are within the "Staff" ou. There will probably a
few extraneous groups out there and should be ignored.

Also, the mirroring system over-writes local permissions with LDAP ones when a user logs in.
For example, say a user is not part of the event admin LDAP group, but is
made part of the event admin DJANGO group by a super user. The user will show
up as an option as an Event Admin in the Add an Event page, and for all practical
purposes will be an Event Admin - until his/her account is synced with LDAP on
login. When that happens, the user will be stripped of event admin permissions on the site until he/she is
actually added to the correct group on the LDAP end and the site is synced with
LDAP.

Moral of the story, make changes on the LDAP end first. After you make a
change, get the user to log in for the changes to take effect OR manually go in
to the admin page and update the user's permissions (they will still be
over-written on log in, but there won't be any change) OR run the sync scripts
i've provided.

There are 5 important security groups to consider.

The following groups **inherently** grant user's specific abilities *just by being members of them*.
These abilities are described in their corresponding sections below.

But if you click on the groups in the admin page and look at the permissions that they
propagate, you'll see that some by default they grant none. You can customize what
additional permissions users can get here.

For example, the Intranet_Admin_Access group just grants users the ability to log
in to the admin page. Users who get this ability will probably want the
ability to edit certain objects in the database too, and this is the kind of permission
that can be customized here.

Staff
-----

cn=Staff,ou=staff,dc=campus,dc=bishopblanchet,dc=org

This security group contains all of BBHS's staff. It is also the requirement
for authentication. If a user doesn't belong to this security group, the user
can't log in even if they have the correct username and password.

All members that authenticate via LDAP will be members of this group.

All members of this group get permission to sign up, and unsign up from events.

Chaperone_Requirement
---------------------

cn=Chaperone_Requirement,ou=Intranet,ou=Technology,ou=Staff,dc=campus,dc=bishopblanchet,dc=org

A user will not get any monthly email reminders of their chaperone obligation unless
they are a part of this group. This security group needs to be populated with
all of the teachers.

Chaperone_Site_Admin
--------------------

Members of this group will be granted elevated permission to add, modify, and
delete any Chaperone objects in the database.

They will also get the ability to pull user reports.

In other words they have permission to do anything that is related to the
chaperone app.

Additionally, they can edit user info in the admin page such as change a user's
event unit requirement.

Joan Thompson is probably the only person who needs this access.

Make sure to add her to the Intranet_Admin_Access so she can access the admin
page.

Intranet_Admin_Access
---------------------

cn=Intranet_Admin_Access,ou=Intranet,ou=Technology,ou=Staff,dc=campus,dc=bishopblanchet,dc=org

Joining this group grants users the permission to log in to the admin page at
http://faculty.bishpoblanchet.org/admin/, but nothing more (by default).

Intranet_Super_Admin
--------------------

cn=Intranet_Super_Admin,ou=Intranet,ou=Technology,ou=staff,dc=campus,dc=bishopblanchet,dc=org

Members of this group get full global permission to do anything in the site.

The only exception to the unfettered power that comes from being a member of
this group is the ability to log in to the admin page (which is essential for a
"super user"). To be able to do that, 
**a super user also needs to be a member of
the Intranet_Admin_Acess group.**

Chaperone_Event_Manager
-----------------------

cn=Chaperone_Event_Manager,ou=Intranet,ou=Technology,ou=Staff,dc=campus,dc=bishopblanchet,dc=org

Joining this group allows users to be Event Administrators. All members of this
group will show up in the dropdown menu for Event Administrator in the "Add a
new Event" page.

Scripts
=======

I wrote a few administrative scripts that will come in handy.
They are located in ~/bbhs_intranet/scripts/

syncUser.py
-----------

This script will synchronize the selected user's information from the active
directory with the intranet database.

Run this script immediately after making changes to the LDAP groups in order to
apply the changes immediately on the intranet side.

If you don't, then the changes won't happen until the user who has had his/her
permissions modified next logs in.

For some reason, the AD is a bit laggy in updating information and it sometimes
won't update it's query responses for about 30 seconds after the change.

Make sure the changes have in fact taken place, and if not, then keep running
this script till they do.

Call this script like so::

$ python syncUser.py luisadmin

syncGroup.py
------------

This script does the exact same thing as syncUser.py, but it is designed to be
used for groups instead of individual users.

You can sync ou's and security groups with this script.

Just run it and follow the instructions it gives you.

reset.py
--------

This is a python script I wrote for resetting certain parts of the website.

For example, say you want to erase all of the events in the database, or all of
the users, etc...


manual_reset_db.sh
------------------

This script is a hard reset.

Itactually deletes the database and creates a new one.

Only use this if the database is somehow totally hosed and you don't mind
losing your data.

Other
-----

There are a few other scripts here that were used for development and/or are
obsolete. 

They won't do any harm, but don't use them anyways.

They are:
    * defaults.py
    * permissions.py
    * popFaculty.py



