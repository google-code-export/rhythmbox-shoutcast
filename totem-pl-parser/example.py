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
