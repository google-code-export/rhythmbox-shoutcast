# Introduction #

Here is a bit complicate logic in the plugin. SHOUTcast server can broke all stations ID's, and at the same time we need keep user preferencies (favorite stations). So, i need to explain rhyththmdb database structure.

# Details #

All entrys are the same type;

All stations related to one virtual genre entry. If genre gone from the shoutcast server it is gone from rhythmdb with all stations related to it. Except it do not delete it self if a favorite station here in the list. And, of course, it won't delete favorite stations.

## Genres ##

Genres entrys (has no data, just for navigation) has an unique URL: http://yp.shoutcast.com/sbin/newxml.phtml?genre=%s

## Stations ##
Stations entrys has an unique URL: http://yp.shoutcast.com/sbin/tunein-station.pls?id=%d&genre=%s

Update process make all stations with 'old' keyword. And remove all stations with this tag after update process. So, if something happens during update process, app or db crashed we can find those stations later.

All favorite stations has an 'star' keyword.

After 1.6.0 version:

I decided to change all favorite stations URL to the following. If favorite station playlist is succesfuly loaded to data directory, we change station URL to the new local form: [file://[app](file://[app) data dir]/id=%d&genre=%s&star=%s. Which keeps favorite station hardly.