import rhythmdb
import xml.sax, xml.sax.handler
import shutil

from xmlloader import XmlLoader

class XmlGenreLoader(XmlLoader):
  
  def __init__(self, db):
    self.db = db
    
    self.file_local = os.path.join(cache_dir, 'genres.xml')
    self.file_local_temp = os.path.join(self.file_local, '.tmp')
    self.file_url = 'http://yp.shoutcast.com/sbin/newxml.phtml'
    self.xml_handler = XmlGenreHandler(self.db, self.entry_type)

  def clean(self):
    self.db.entry_foreach_by_type(entry_type, self.clean_keywords)

  def clean_keywords(self, entry):
    self.db.entry_keyword_remove(entry, 'new')

  def remove(self):
    self.db.entry_foreach_by_type(entry_type, self.remove_old)
    
  def remove_old(self, entry):
    self.db.entry_keyword_has(entry, 'new')

  def update(self):
    self.clean()
    XmlLoader.update(self)
    
  def change_idle_cb(self):
    if(self.updating == True):
      self.remove()
