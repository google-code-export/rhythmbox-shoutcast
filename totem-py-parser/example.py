import totem_py_parser

def pl_entry(parser, uri, htable):
  print 'uri: ' + uri
  print 'title: ' + htable.lookup('title').__str__()
  print 'genre: ' + htable.lookup('genre').__str__()

def parse_uri(uri):
  parser = totem_py_parser.TotemPyParser()
  parser.connect('entry-py-parsed', pl_entry)
  #g_object_set (parser, "recurse", FALSE, NULL);

  res = parser.parse(uri, False)
  
  return res

print parse_uri('http://yp.shoutcast.com/sbin/tunein-station.pls?id=9492')
