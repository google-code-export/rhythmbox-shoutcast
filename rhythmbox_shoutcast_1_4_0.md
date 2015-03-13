# rhythmbox-shoutcast-1.4.0 #

works well!

# Changes 1.4.1 #
  * add metadata info to the title (thanks to Marcelo Schüler for the report)

# Changes 1.4.0 #

**New features**
  * added new styles to genres window (gray)
  * Fix genre counters (-1 to each)
  * move plugin to the Library group (from the Internet group)

# Screenshots #

![http://wiki.rhythmbox-shoutcast.googlecode.com/git/rhythmbox_shoutcast_1_4_0/Screenshot-Music%20Player.png](http://wiki.rhythmbox-shoutcast.googlecode.com/git/rhythmbox_shoutcast_1_4_0/Screenshot-Music%20Player.png)

# Bugs #

You can see warning message about bug in rhythmdb when you select Shoutcast plugin from notepad widget. What does this bug do?

Any Rhythmbox plugin can not operate with database (rhythmdb) until it fully loaded. But here in API is no function which can test database state to be ensure database is fully loaded.

So, for most cases i can ignore this API restriction by register rhyhmdb signal called 'load-complete'. Database emit this signal to everyone who was already connected. But that is not true for new added plugin by configuration manager. For example if you just downloaded plugin and add it to rhtyhmbox (set checkbox in Plugin managed) here is no way to determinate database state and no way to be sure write to database is safe.

So i desided to show those warning message until rhythmbox/rhythmdb will fix this issue.

https://bugzilla.gnome.org/show_bug.cgi?id=612207