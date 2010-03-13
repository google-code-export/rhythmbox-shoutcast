import rhythmdb, rb

import traceback, sys

from db import *

def fe():
  result = ''
  
  lines = traceback.format_exception(sys.exc_type, sys.exc_value, sys.exc_traceback)
  for line in lines:
    result += line
    
  return Exception(result)

def entry_to_string(db, entry):
  print "id: " + repr(db.entry_get(entry, rhythmdb.PROP_ENTRY_ID))
  print "title: " + repr(db.entry_get(entry, rhythmdb.PROP_TITLE))
  print "genre: " + repr(db.entry_get(entry, rhythmdb.PROP_GENRE))
  print "url: " + repr(db.entry_get(entry, rhythmdb.PROP_LOCATION))
  print "keyword: " + repr(db.entry_get(entry, rhythmdb.PROP_KEYWORD))

def log(log):
  print log
