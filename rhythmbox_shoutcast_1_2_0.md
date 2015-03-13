# rhythmbox-shoutcast-1.2.0 #

works well!

# Changes 1.2.3 #
  * add manual reload genres / stations
  * fix favorite button (bad high-light stations)
  * fix database crash

# Changes 1.2.2 #
  * fix package version

# Changes 1.2.1 #
  * fix version check

# Changes 1.2.0 #

New features:
  * Add online version check to this release
  * add favorite stations filter
  * add copy clipboard station url feature
  * add status notification messages
  * add save view/postion to stations/genres lists


# Screenshots #

![http://wiki.rhythmbox-shoutcast.googlecode.com/git/rhythmbox_shoutcast_1_2_0/Screenshot-PsyChill%20-%20D%20I%20G%20I%20T%20A%20L%20L%20Y%20-%20I%20M%20P%20O%20R%20T%20E%20D%20-%20downtempo%20psychedelic%20dub%20grooves,%20goa%20ambient,%20and%20-%20%5BSHOUTcast.com%5D.png](http://wiki.rhythmbox-shoutcast.googlecode.com/git/rhythmbox_shoutcast_1_2_0/Screenshot-PsyChill%20-%20D%20I%20G%20I%20T%20A%20L%20L%20Y%20-%20I%20M%20P%20O%20R%20T%20E%20D%20-%20downtempo%20psychedelic%20dub%20grooves,%20goa%20ambient,%20and%20-%20%5BSHOUTcast.com%5D.png)

# Bugs #

You can see warning message about bug in rhythmdb when you select Shoutcast plugin from notepad widget. What does this bug do?

Any Rhythmbox plugin can not operate with database (rhythmdb) until it fully loaded. But here in API is no function which can test database state to be ensure database is fully loaded.

So, for most cases i can ignore this API restriction by register rhyhmdb signal called 'load-complete'. Database emit this signal to everyone who was already connected. But that is not true for new added plugin by configuration manager. For example if you just downloaded plugin and add it to rhtyhmbox (set checkbox in Plugin managed) here is no way to determinate database state and no way to be sure write to database is safe.

So i desided to show those warning message until rhythmbox/rhythmdb will fix this issue.

https://bugzilla.gnome.org/show_bug.cgi?id=612207