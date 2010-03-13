import rhythmdb
import xml.sax, xml.sax.handler
import shutil
import os

from xmlloader import *
from xmlstationshandler import *
from db import *
from debug import *

class XmlStationsLoader(XmlLoader):

  def __init__(self, db, cache_dir, entry_type, genre):
    XmlLoader.__init__(self, os.path.join(cache_dir, 'stations-%s.xml' % genre),
                       'http://yp.shoutcast.com/sbin/newxml.phtml?genre=%s' % genre)
    self.db = db
    self.entry_type = entry_type
    self.genre = genre

    self.xml_handler = XmlStationsHandler(self.db, self.entry_type, genre)

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
    entry = iter_to_entry(self.db, query_model, iter)
    
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
    entry = iter_to_entry(self.db, model, iter)

    entry_to_string(self.db, entry)

    self.db.entry_delete(entry)
    
    return False
