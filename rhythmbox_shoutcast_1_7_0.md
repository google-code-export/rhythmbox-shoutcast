# rhythmbox-shoutcast-1.7.0 #

works well!

# Changes 1.7.2 #
  * fix save\_to\_disk property

# Changes 1.7.1 #
  * new version check url

# Changes 1.7.0 #
  * fix new rhythmbox 0.13 db api

# Screenshots #

  * New icon scheme, dynamic columns (introduces in 1.6.0)

![http://wiki.rhythmbox-shoutcast.googlecode.com/git/rhythmbox_shoutcast_1_6_0/Screenshot-Music%20Player-1.png](http://wiki.rhythmbox-shoutcast.googlecode.com/git/rhythmbox_shoutcast_1_6_0/Screenshot-Music%20Player-1.png)

![http://wiki.rhythmbox-shoutcast.googlecode.com/git/rhythmbox_shoutcast_1_6_0/Screenshot-Music%20Player.png](http://wiki.rhythmbox-shoutcast.googlecode.com/git/rhythmbox_shoutcast_1_6_0/Screenshot-Music%20Player.png)

  * Import/Export feature (introduced in 1.5.0)

![http://wiki.rhythmbox-shoutcast.googlecode.com/git/rhythmbox_shoutcast_1_5_0/Screenshot-M%C3%A9lodisque.png](http://wiki.rhythmbox-shoutcast.googlecode.com/git/rhythmbox_shoutcast_1_5_0/Screenshot-M%C3%A9lodisque.png)

  * Smart search (introduced in 1.3.0)

![http://wiki.rhythmbox-shoutcast.googlecode.com/git/rhythmbox_shoutcast_1_5_0/Screenshot-M%C3%A9lodisque%20-%20Vari%C3%A9t%C3%A9s%20et%20Chansons%20Fran%C3%A7aises%20%28Melodisque%20-%20%5BSHOUTcast.com%5D%29.png](http://wiki.rhythmbox-shoutcast.googlecode.com/git/rhythmbox_shoutcast_1_5_0/Screenshot-M%C3%A9lodisque%20-%20Vari%C3%A9t%C3%A9s%20et%20Chansons%20Fran%C3%A7aises%20%28Melodisque%20-%20%5BSHOUTcast.com%5D%29.png)

  * Copy URL (introduced in 1.2.0)

![http://wiki.rhythmbox-shoutcast.googlecode.com/git/rhythmbox_shoutcast_1_5_0/Screenshot-Jean-Pierre%20MILLERS%20-%20Rendez-vous%20%28Melodisque%20-%20%5BSHOUTcast.com%5D%29.png](http://wiki.rhythmbox-shoutcast.googlecode.com/git/rhythmbox_shoutcast_1_5_0/Screenshot-Jean-Pierre%20MILLERS%20-%20Rendez-vous%20%28Melodisque%20-%20%5BSHOUTcast.com%5D%29.png)

  * Manual reload stations / genres (introduced in 1.2.3)

![http://wiki.rhythmbox-shoutcast.googlecode.com/git/rhythmbox_shoutcast_1_5_0/Screenshot-M%C3%A9lodisque%20-%20Vari%C3%A9t%C3%A9s%20et%20Chansons%20Fran%C3%A7aises%20%28Melodisque%20-%20%5BSHOUTcast.com%5D%29-1.png](http://wiki.rhythmbox-shoutcast.googlecode.com/git/rhythmbox_shoutcast_1_5_0/Screenshot-M%C3%A9lodisque%20-%20Vari%C3%A9t%C3%A9s%20et%20Chansons%20Fran%C3%A7aises%20%28Melodisque%20-%20%5BSHOUTcast.com%5D%29-1.png)


# Bugs #

You can see warning message about bug in rhythmdb when you select Shoutcast plugin from notepad widget. What does this bug do?

Any Rhythmbox plugin can not operate with database (rhythmdb) until it fully loaded. But here in API is no function which can test database state to be ensure database is fully loaded.

So, for most cases i can ignore this API restriction by register rhyhmdb signal called 'load-complete'. Database emit this signal to everyone who was already connected. But that is not true for new added plugin by configuration manager. For example if you just downloaded plugin and add it to rhtyhmbox (set checkbox in Plugin managed) here is no way to determinate database state and no way to be sure write to database is safe.

So i desided to show those warning message until rhythmbox/rhythmdb will fix this issue.

https://bugzilla.gnome.org/show_bug.cgi?id=612207