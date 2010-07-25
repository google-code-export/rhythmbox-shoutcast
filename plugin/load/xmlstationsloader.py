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
import xml.sax, xml.sax.handler, shutil, os
import rbdb, debug

from xmlloader import *
from xmlstationshandler import *
from xmlgenreshandler import *

class XmlStationsLoader(XmlLoader):

  def __init__(self, db, cache_dir, data_dir, entry_type, genre):
    XmlLoader.__init__(self, os.path.join(cache_dir, 'stations-%s.xml' % (urllib.quote(genre))),
                       xmlgenres_encodeurl(genre))
    self.db = db
    self.entry_type = entry_type
    self.genre = genre

    self.xml_handler = XmlStationsHandler(self.db, self.entry_type, genre, data_dir)

  def loader_get_progress(self):
    if self.check_progress():
      return ('downloading: ' + self.genre, self.check_get_progress()[1])
    else:
      return ('parsing: ' + self.genre, XmlLoader.loader_get_progress(self)[1])

  def clean_keywords(self):
    query = self.db.query_new()
    self.db.query_append(query, (rhythmdb.QUERY_PROP_EQUALS, rhythmdb.PROP_TYPE, self.entry_type))
    self.db.query_append(query, (rhythmdb.QUERY_PROP_EQUALS, rhythmdb.PROP_GENRE, self.genre))
    self.db.query_append(query, (rhythmdb.QUERY_PROP_LIKE, rhythmdb.PROP_KEYWORD, "station"))

    query_model = self.db.query_model_new_empty()
    self.db.do_full_query_parsed(query_model, query)
    
    query_model.foreach(self.clean_keywords_db)
    self.db.commit()

  def clean_keywords_db(self, query_model, path, iter):
    entry = rbdb.iter_to_entry(self.db, query_model, iter)
    
    self.db.entry_keyword_add(entry, 'old')

    return False
    
  def remove_old(self):
    query = self.db.query_new()
    self.db.query_append(query, (rhythmdb.QUERY_PROP_EQUALS, rhythmdb.PROP_TYPE, self.entry_type))
    self.db.query_append(query, (rhythmdb.QUERY_PROP_EQUALS, rhythmdb.PROP_GENRE, self.genre))
    self.db.query_append(query, (rhythmdb.QUERY_PROP_LIKE, rhythmdb.PROP_KEYWORD, "station"))
    self.db.query_append(query, (rhythmdb.QUERY_PROP_LIKE, rhythmdb.PROP_KEYWORD, 'old'))
    self.db.query_append(query, (rhythmdb.QUERY_PROP_NOT_LIKE, rhythmdb.PROP_KEYWORD, 'star'))
    query_model = self.db.query_model_new_empty()
    self.db.do_full_query_parsed(query_model, query)

    query_model.foreach(self.remove_keywords_db)
    self.db.commit()

  def remove_keywords_db(self, model, path, iter):
    entry = rbdb.iter_to_entry(self.db, model, iter)

    debug.log("Remove old station: " + repr(self.db.entry_get(entry, rhythmdb.PROP_TITLE)))

    self.db.entry_delete(entry)
    
    return False
