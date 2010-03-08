import rhythmdb, rb

from db import *

def entry_to_string(db, entry):
  print "id: " + repr(db.entry_get(entry, rhythmdb.PROP_ENTRY_ID))
  print "title: " + repr(db.entry_get(entry, rhythmdb.PROP_TITLE))
  print "genre: " + repr(db.entry_get(entry, rhythmdb.PROP_GENRE))
  print "url: " + repr(db.entry_get(entry, rhythmdb.PROP_LOCATION))
  print "keyword: " + repr(db.entry_get(entry, rhythmdb.PROP_KEYWORD))
