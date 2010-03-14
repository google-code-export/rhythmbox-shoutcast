import rhythmdb
import xml.sax, xml.sax.handler
import shutil
import os, os.path

from xmlloader import *
from xmlgenreshandler import *
from db import *
from debug import *

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
    entry = iter_to_entry(self.db, model, iter)
    
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
    entry = iter_to_entry(self.db, model, iter)

    genre = self.db.entry_get(entry, rhythmdb.PROP_GENRE)
    
    query = self.db.query_new()
    self.db.query_append(query, (rhythmdb.QUERY_PROP_EQUALS, rhythmdb.PROP_TYPE, self.entry_type))
    self.db.query_append(query, (rhythmdb.QUERY_PROP_EQUALS, rhythmdb.PROP_GENRE, genre))
    self.db.query_append(query, (rhythmdb.QUERY_PROP_LIKE, rhythmdb.PROP_KEYWORD, 'station'))
    self.db.query_append(query, (rhythmdb.QUERY_PROP_LIKE, rhythmdb.PROP_KEYWORD, 'star'))
    query_model = self.db.query_model_new_empty()
    self.db.do_full_query_parsed(query_model, query)
    stars_amount = query_model.get_size()

    # remove 'genre' only if here no favorite stations left
    if stars_amount == 0:
      print "Remove old genre's: " + genre
      entry_to_string(self.db, entry)
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
    entry = iter_to_entry(self.db, model, iter)

    self.db.entry_delete(entry)
    
    return False
