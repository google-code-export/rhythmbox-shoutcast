import rhythmdb
import xml.sax, xml.sax.handler
import shutil

from xmlloader import XmlLoader

class XmlGenreLoader(XmlLoader):
  
  def __init__(self):
    self.file_local = os.path.join(cache_dir, 'genres.xml')
    self.file_local_temp = os.path.join(self.file_local, '.tmp')
    self.file_url = 'http://yp.shoutcast.com/sbin/newxml.phtml'
    self.xml_handler = XmlGenreHandler(self.db, self.entry_type)