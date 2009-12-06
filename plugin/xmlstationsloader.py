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

    self.file_dir = cache_dir
    self.file_local = os.path.join(cache_dir, 'stations-%s.xml' % genre)
    self.file_local_temp = self.file_local + '.tmp'
    self.file_url = 'http://yp.shoutcast.com/sbin/newxml.phtml?genre=%s' % genre
    self.xml_handler = XmlStationsHandler(self.db, self.entry_type, genre)
