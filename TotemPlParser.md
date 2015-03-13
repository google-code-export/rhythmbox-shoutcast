# Introduction #

totem-pl-parser library allow to parse all playlists range supported by totem player. it really wide rang.

out task is to get this library work with our plugin.

fortunately totem-pl-parser use gobject as base for each class in it. so we can easily translate all code to pyton just by pygobject-codegen-2.0 utility.

unfortunately totem-pl-parser use marshaled class in callback function (a hash table). so we can't use codegen algorithm to use it directly.

  * [similar problem within rhythmbox](https://bugzilla.gnome.org/show_bug.cgi?id=412210)

let me show this part of code:

python example:
```
import totem_pl_parser

def pl_entry(parser, uri, htable):
  title = htable['title'];
  #genre = htable.lookup (metadata, TOTEM_PL_PARSER_FIELD_GENRE);
  print uri, htable
  print htable.__class__()

def parse_uri(uri):
  parser = totem_pl_parser.TotemPlParser()
  print dir(parser)
  parser.connect('entry-parsed', pl_entry)
  #g_object_set (parser, "recurse", FALSE, NULL);

  res = parser.parse(uri, False)

  if res == totem_pl_parser.TOTEM_PL_PARSER_RESULT_UNHANDLED:
    return
  if res == totem_pl_parser.TOTEM_PL_PARSER_RESULT_IGNORED:
    return

  if res == totem_pl_parser.TOTEM_PL_PARSER_RESULT_SUCCESS:
    return
  if res == totem_pl_parser.TOTEM_PL_PARSER_RESULT_ERROR:
    return

parse_uri('http://yp.shoutcast.com/sbin/tunein-station.pls?id=9492')
```

so, we have one signal 'entry-parsed', which should drop more info about entry to our code. here is signal description:

```
static void
entry_parsed (TotemPlParser *parser, const char *uri,
	      GHashTable *metadata, gpointer data)
{
	g_print ("added URI '%s'\n", uri);
	g_hash_table_foreach (metadata, (GHFunc) entry_metadata_foreach, NULL);
}
```

so we allow to:
  * create selfown pyton library to parse playlists (bad way)
  * fix bug in pygobject library (which required to rebuild system library, bad)
  * add some magic on fly type converter to pygobject, if library allow it
  * add new wrapper class to totem-pl-parser main class with duplicated signals/functions
  * migrate to gnome pygobject version http://live.gnome.org/PyGObject

# Source #

You can find source code of my work here:

http://code.google.com/p/rhythmbox-shoutcast/source/browse/#git/totem-py-parser