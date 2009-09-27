import rhythmdb
import xml.sax, xml.sax.handler
import shutil
import os, os.path

from xmlloader import XmlLoader
from xmlgenrehandler import XmlGenreHandler

class XmlGenreLoader(XmlLoader):

  def __init__(self, db, cache_dir, entry_type_s):
    self.db = db
    self.entry_type = entry_type_s
    
    print "DIR IS" + cache_dir
    
    self.file_local = os.path.join(cache_dir, 'genres.xml')
    self.file_local_temp = os.path.join(self.file_local, '.tmp')
    self.file_url = 'http://yp.shoutcast.com/sbin/newxml.phtml'
    self.xml_handler = XmlGenreHandler(self.db, self.entry_type)
