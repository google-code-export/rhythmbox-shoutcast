"""
  rhythmbox-shoutcast plugin for rhythmbox application.
  Copyright (C) 2009  Alexey Kuznetsov <ak@axet.ru>
  
  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.
  
  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.
  
  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

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
