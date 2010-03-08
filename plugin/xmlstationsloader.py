import rhythmdb
import xml.sax, xml.sax.handler
import shutil
import os

from xmlloader import XmlLoader
from xmlstationshandler import XmlStationsHandler

class XmlStationsLoader(XmlLoader):

  def __init__(self, db, cache_dir, entry_type, genre):
    self.db = db
    self.entry_type = entry_type
    self.genre = genre

    self.file_dir = cache_dir
    self.file_local = os.path.join(cache_dir, 'stations-%s.xml' % genre)
    self.file_local_temp = self.file_local + '.tmp'
    self.file_url = 'http://yp.shoutcast.com/sbin/newxml.phtml?genre=%s' % genre
    self.xml_handler = XmlStationsHandler(self.db, self.entry_type, genre)

  def iter_to_entry(self, model, iter):
    return model.get(iter, 0)[0]

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
    entry = self.iter_to_entry(query_model, iter)
    
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
    entry = self.iter_to_entry(model, iter)

    self.db.entry_delete(entry)
    
    return False
