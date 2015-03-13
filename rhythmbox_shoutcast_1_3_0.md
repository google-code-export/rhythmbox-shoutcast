# rhythmbox-shoutcast-1.3.0 #

works well!

# Changes 1.3.2 #
  * fix upper window fast search
  * fix setup script possible source missmuch
  * small entrysearch bar fix

# Changes 1.3.1 #
  * micro fix for version check

# Changes 1.3.0 #
  * fix song double click

**New features**
  * align favorite icon to center and set column size to icon size
  * new icon color (b&w)
  * smartsearch
  * sorting by title


# Screenshots #

![http://wiki.rhythmbox-shoutcast.googlecode.com/git/rhythmbox_shoutcast_1_3_0/Screenshot-Classic%20EuroDance%20-%20D%20I%20G%20I%20T%20A%20L%20L%20Y%20-%20I%20M%20P%20O%20R%20T%20E%20D%20-%20Finest%20imported%20cheese%20on%20the%20net!%20-%20%5BSHOUTcast.com%5D.png](http://wiki.rhythmbox-shoutcast.googlecode.com/git/rhythmbox_shoutcast_1_3_0/Screenshot-Classic%20EuroDance%20-%20D%20I%20G%20I%20T%20A%20L%20L%20Y%20-%20I%20M%20P%20O%20R%20T%20E%20D%20-%20Finest%20imported%20cheese%20on%20the%20net!%20-%20%5BSHOUTcast.com%5D.png)

# Bugs #

You can see warning message about bug in rhythmdb when you select Shoutcast plugin from notepad widget. What does this bug do?

Any Rhythmbox plugin can not operate with database (rhythmdb) until it fully loaded. But here in API is no function which can test database state to be ensure database is fully loaded.

So, for most cases i can ignore this API restriction by register rhyhmdb signal called 'load-complete'. Database emit this signal to everyone who was already connected. But that is not true for new added plugin by configuration manager. For example if you just downloaded plugin and add it to rhtyhmbox (set checkbox in Plugin managed) here is no way to determinate database state and no way to be sure write to database is safe.

So i desided to show those warning message until rhythmbox/rhythmdb will fix this issue.

https://bugzilla.gnome.org/show_bug.cgi?id=612207