import rhythmdb
import xml.sax, xml.sax.handler
import shutil

from xmlloader import XmlLoader

class XmlStationsLoader(XmlLoader):

  db = None
  shell = None
  entry_type = None
  
  file_local = None
  file_local_temp = None
  file_url = None
  
  def __init__(self, genre, cache_dir):
    self.file_local = os.path.join(cache_dir, 'stations-%s.xml' % genre)
    self.file_local_temp = os.path.join(self.file_local, '.tmp')
    self.file_url = 'http://yp.shoutcast.com/sbin/newxml.phtml?genre=%s' % genre

