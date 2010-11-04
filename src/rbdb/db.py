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