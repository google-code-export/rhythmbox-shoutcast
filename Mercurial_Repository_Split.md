_**./map**_
```
include totem-py-parser
include totem-pl-parser
include totem-playlist-parser
rename totem-py-parser .
```


_# hg convert --filemap map rhythmbox-shoutcast/ totem-py-parser/ -r 44b87b4eb428_

_**./rhythmbox-shoutcast/.hgsub**_
```
totem-py-parser = https://totem-py-parser.rhythmbox-shoutcast.googlecode.com/hg/
```