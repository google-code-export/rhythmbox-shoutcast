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

from xmlloader import *
from xmlgenreshandler import *

class XmlGenresLoader(XmlLoader):

  def __init__(self, db, cache_dir, entry_type):
    XmlLoader.__init__(self, os.path.join(cache_dir, 'genres.xml'),
                       'http://yp.shoutcast.com/sbin/newxml.phtml')

    self.db = db
    self.entry_type = entry_type
    
    self.xml_handler = XmlGenresHandler(self.db, self.entry_type)

  def loader_get_progress(self):
    if self.check_progress():
      return ('downloading genres', self.check_get_progress()[1])
    else:
      return ('parsing genres', XmlLoader.loader_get_progress(self)[1])

  def clean_keywords(self):
    query = self.db.query_new()
    self.db.query_append(query, (rhythmdb.QUERY_PROP_EQUALS, rhythmdb.PROP_TYPE, self.entry_type))
    self.db.query_append(query, (rhythmdb.QUERY_PROP_LIKE, rhythmdb.PROP_KEYWORD, 'genre'))
    query_model = self.db.query_model_new_empty()
    self.db.do_full_query_parsed(query_model, query)
    
    query_model.foreach(self.clean_keywords_db)
    self.db.commit()

  def clean_keywords_db(self, model, path, iter):
    entry = rbdb.iter_to_entry(self.db, model, iter)
    
    self.db.entry_keyword_add(entry, 'old')

    return False

  def remove_old(self):
    query = self.db.query_new()
    self.db.query_append(query, (rhythmdb.QUERY_PROP_EQUALS, rhythmdb.PROP_TYPE, self.entry_type))
    self.db.query_append(query, (rhythmdb.QUERY_PROP_LIKE, rhythmdb.PROP_KEYWORD, 'genre'))
    self.db.query_append(query, (rhythmdb.QUERY_PROP_LIKE, rhythmdb.PROP_KEYWORD, 'old'))
    query_model = self.db.query_model_new_empty()
    self.db.do_full_query_parsed(query_model, query)

    query_model.foreach(self.remove_old_db)
    self.db.commit()

  def remove_old_db(self, model, path, iter):
    entry = rbdb.iter_to_entry(self.db, model, iter)

    genre = self.db.entry_get(entry, rhythmdb.PROP_GENRE)
    
    query = self.db.query_new()
    self.db.query_append(query, (rhythmdb.QUERY_PROP_EQUALS, rhythmdb.PROP_TYPE, self.entry_type))
    self.db.query_append(query, (rhythmdb.QUERY_PROP_EQUALS, rhythmdb.PROP_GENRE, genre))
    self.db.query_append(query, (rhythmdb.QUERY_PROP_LIKE, rhythmdb.PROP_KEYWORD, 'station'))
    self.db.query_append(query, (rhythmdb.QUERY_PROP_LIKE, rhythmdb.PROP_KEYWORD, 'star'))
    query_model = self.db.query_model_new_empty()
    self.db.do_full_query_parsed(query_model, query)
    stars_here = query_model.get_iter_first()

    # remove 'genre' only if here no favorite stations left
    if not stars_here:
      debug.log("Remove old genre and all stations related to it: " + genre)
      self.db.entry_delete(entry)

    query = self.db.query_new()
    self.db.query_append(query, (rhythmdb.QUERY_PROP_EQUALS, rhythmdb.PROP_TYPE, self.entry_type))
    self.db.query_append(query, (rhythmdb.QUERY_PROP_EQUALS, rhythmdb.PROP_GENRE, genre))
    self.db.query_append(query, (rhythmdb.QUERY_PROP_LIKE, rhythmdb.PROP_KEYWORD, 'station'))
    self.db.query_append(query, (rhythmdb.QUERY_PROP_NOT_LIKE, rhythmdb.PROP_KEYWORD, 'star'))
    query_model = self.db.query_model_new_empty()
    self.db.do_full_query_parsed(query_model, query)
    query_model.foreach(self.remove_stations_db)
    
    return False

  def remove_stations_db(self, model, path, iter):
    entry = rbdb.iter_to_entry(self.db, model, iter)

    debug.log("Remove old genre and all stations related to it: " + repr(self.db.entry_get(entry, rhythmdb.PROP_TITLE)))
    self.db.entry_delete(entry)
    
    return False
