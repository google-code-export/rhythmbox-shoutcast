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

import rhythmdb
import xml.sax, xml.sax.handler, shutil, os, os.path
import rbdb, debug

# one more check requred: items not marked as station or genre

def check_for_damage(db, entry_type):
  query = db.query_new()
  db.query_append(query, (rhythmdb.QUERY_PROP_EQUALS, rhythmdb.PROP_TYPE, entry_type))
  db.query_append(query, (rhythmdb.QUERY_PROP_LIKE, rhythmdb.PROP_KEYWORD, 'genre'))
  db.query_append(query, (rhythmdb.QUERY_PROP_LIKE, rhythmdb.PROP_KEYWORD, 'station'))
  query_model = db.query_model_new_empty()
  db.do_full_query_parsed(query_model, query)

  check = query_model.get_iter_first()
  return bool(check)

def check_and_serve(db, entry_type):
  if check_for_damage(db, entry_type):
    debug.log('Database damaged, clean ALL')
    delete_all(db, entry_type)

def delete_all(db, entry_type):
  db.entry_delete_by_type(entry_type)
