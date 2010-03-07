import rhythmdb
import xml.sax, xml.sax.handler
import shutil
import os, os.path

from xmlloader import XmlLoader
from xmlgenreshandler import XmlGenresHandler

class XmlGenresLoader(XmlLoader):

  def __init__(self, db, cache_dir, entry_type):
    self.db = db
    self.entry_type = entry_type
    
    self.file_dir = cache_dir
    self.file_local = os.path.join(cache_dir, 'genres.xml')
    self.file_local_temp = self.file_local + '.tmp'
    self.file_url = 'http://yp.shoutcast.com/sbin/newxml.phtml'
    self.xml_handler = XmlGenresHandler(self.db, self.entry_type)

  def clean_keywords(self):
    query = self.db.query_new()
    self.db.query_append(query, (rhythmdb.QUERY_PROP_EQUALS, rhythmdb.PROP_TYPE, self.entry_type))
    self.db.query_append(query, (rhythmdb.QUERY_PROP_LIKE, rhythmdb.PROP_KEYWORD, 'genre'))

    query_model = self.db.query_model_new_empty()
    self.db.do_full_query_parsed(query_model, query)
    
    query_model.foreach(self.clean_keywords_db)

  def clean_keywords_db(self, model, path, iter):
    entry = model.tree_path_to_entry(path)
    
    loader.db.entry_keyword_add(entry, 'old')
    loader.db.entry_keyword_remove(entry, 'new')
    
    return True
    
  def remove_old(self):
    query = self.db.query_new()
    self.db.query_append(query, (rhythmdb.QUERY_PROP_EQUALS, rhythmdb.PROP_TYPE, entry_type))
    self.db.query_append(query, (rhythmdb.QUERY_PROP_LIKE, rhythmdb.PROP_KEYWORD, 'genre'))
    self.db.query_append(query, (rhythmdb.QUERY_PROP_LIKE, rhythmdb.PROP_KEYWORD, 'old'))

    query_model = self.db.query_model_new_empty()
    self.db.do_full_query_parsed(query_model, self.query)

    query_model.gtk_tree_model_foreach(remove_keywords_db)

  def remove_old_db(self, model, path, iter):
    entry = model.tree_path_to_entry(path)

    query = self.db.query_new()
    self.db.query_append(query, (rhythmdb.QUERY_PROP_EQUALS, rhythmdb.PROP_TYPE, self.entry_type))
    self.db.query_append(query, (rhythmdb.QUERY_PROP_EQUALS, rhythmdb.PROP_GENRE, entry.get_string()))
    self.db.query_append(query, (rhythmdb.QUERY_PROP_LIKE, rhythmdb.PROP_KEYWORD, 'station'))
    self.db.query_append(query, (rhythmdb.QUERY_PROP_NOT_LIKE, rhythmdb.PROP_KEYWORD, 'star'))

    query_model = self.db.query_model_new_empty()
    self.db.do_full_query_parsed(query_model, self.query)
    
    query_model.gtk_tree_model_foreach(remove_stations_db)

    query = self.db.query_new()
    self.db.query_append(query, (rhythmdb.QUERY_PROP_EQUALS, rhythmdb.PROP_TYPE, self.entry_type))
    self.db.query_append(query, (rhythmdb.QUERY_PROP_EQUALS, rhythmdb.PROP_GENRE, entry.get_string()))
    self.db.query_append(query, (rhythmdb.QUERY_PROP_LIKE, rhythmdb.PROP_KEYWORD, 'station'))
    self.db.query_append(query, (rhythmdb.QUERY_PROP_LIKE, rhythmdb.PROP_KEYWORD, 'star'))

    query_model = self.db.query_model_new_empty()
    self.db.do_full_query_parsed(query_model, self.query)
    
    # remove 'genre' only if here no favorite stations left
    if query_model.get_size() == 0:
      self.db.entry_remove(entry)
    
    return True

  def remove_stations_db(self, model, path, iter, star):
    entry = model.tree_path_to_entry(path)

    self.db.entry_remove(entry)
    
    return True
