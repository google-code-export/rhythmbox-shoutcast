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
  out = ''
  out += "id: " + repr(db.entry_get(entry, rhythmdb.PROP_ENTRY_ID)) + '\n'
  out += "title: " + repr(db.entry_get(entry, rhythmdb.PROP_TITLE)) + '\n'
  out += "genre: " + repr(db.entry_get(entry, rhythmdb.PROP_GENRE)) + '\n'
  out += "url: " + repr(db.entry_get(entry, rhythmdb.PROP_LOCATION)) + '\n'
  out += "keyword: " + repr(db.entry_get(entry, rhythmdb.PROP_KEYWORD)) + '\n'
  
  print out

def log(log):
  print log
