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

def entry_lookup_by_location(db, url):
  return db.entry_lookup_by_location(url)

def id_to_entry(db, eid):
  entry = db.entry_lookup_by_id(eid)
  
  if not entry:
    raise Exception('iter_to_entry: bad entry ' + repr(eid) + ' ' + repr(id))

  return entry

def entry_to_id(db, entry):
  eid = db.entry_get(entry, rhythmdb.PROP_ENTRY_ID)

  return eid

def iter_to_entry(db, model, iter):
  id = model.get(iter, 0)[0]
  if not id:
    raise Exception('Bad id' + id)
  
  eid = db.entry_get(id, rhythmdb.PROP_ENTRY_ID)
  if not eid:
    raise Exception('Bad eid' + eid)
  
  entry = db.entry_lookup_by_id(eid)
  
  if not entry:
    raise Exception('iter_to_entry: bad entry ' + repr(eid) + ' ' + repr(id))

  return entry

def register_entry_type(db, name):

  if hasattr(db, 'entry_register_type'):
    entry_type = db.entry_register_type(name)

    return entry_type  
  else:
    class ShoutcastEntryType(rhythmdb.EntryType):
      def __init__(self):
        rhythmdb.EntryType.__init__(self, name = name, save_to_disk = True)
        self.can_sync_metadata = True
        self.sync_metadata = None
        self.category = rhythmdb.ENTRY_STREAM
  
    entry_type = ShoutcastEntryType()
    db.register_entry_type(entry_type)
  
    return entry_type