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

import rhythmdb, rb
import xml.sax, xml.sax.handler, shutil, gobject, os, time
import debug

from checkdownload import *

class XmlLoader(CheckDownload):

  db = None
  shell = None
  entry_type = None

  # xml hander for file_local file
  xml_handler = None

  fresh = True
  
  catalogue_loader = None
    
  # exception / error text message
  error = None
  
  __load_current_size = 0
  __load_total_size = 0

  __callback = None
  __notify_id = 0
  
  def __init__(self, file, url):
    CheckDownload.__init__(self, file, url)
    
    self.url = url
    
    self.check_callback(self.download_state)
  
  def loader_progress(self):
    if self.error:
      return False
    
    if self.check_progress():
      return True
   
    if self.catalogue_loader:
      return True
    
    return False

  def loader_callback(self, callback):
    self.__callback = callback

  def loader_fresh(self):
    return self.fresh

  def loader_update(self):
    self.fresh = False
    self.clean_keywords()
    self.update_catalogue()

  def loader_result(self):
    return self.error

  def loader_get_progress(self):
    if self.check_progress():
      return self.check_get_progress()
    else:
      if self.__load_total_size != 0:
        return (self.url, self.__load_current_size / float(self.__load_total_size))
      else:
        return (self.url, -1)

  def set_error(self, e):
    self.error = e

  def download_state(self):
    if self.check_progress():
      return
    
    if self.check_result():
      self.set_error(self.check_result())
      self.__notify_status_changed()
      return
    
    self.catalogue_load()
    self.__notify_status_changed()

  def update_catalogue(self):
    if not self.check_update():
      self.catalogue_load()

  def catalogue_load(self):
    parser = xml.sax.make_parser()
    parser.setContentHandler(self.xml_handler)
    
    self.catalogue_loader = rb.ChunkLoader()
    self.catalogue_loader.get_url_chunks(self.file_local, 10 * 1024, True, self.catalogue_load_chunk_cb, parser)

  def catalogue_load_chunk_close(self, parser):
    parser.close()

    self.updating = False
    self.catalogue_loader = None

    self.db.commit()
    
    self.remove_old()
    
  def close_and_remove(self):
    try:
      debug.log('remove bad xml ' + self.file_local)
      os.remove(self.file_local)
    except:
      pass

  def catalogue_load_chunk_cb(self, result, total, parser):
    try:
      if not result:
        self.catalogue_load_chunk_close(parser)
              
      elif isinstance(result, Exception):
        self.set_error(result)
        
      else:
        parser.feed(result)

        self.__load_current_size += len(result)
        self.__load_total_size = total
    except xml.sax.SAXParseException:
      if self.catalogue_loader:
        self.catalogue_loader.cancel()
      self.close_and_remove()
      self.set_error(service.fe())
    except:
      if self.catalogue_loader:
        self.catalogue_loader.cancel()
      self.set_error(service.fe())

    self.__notify_status_changed()

  def __notify_status_changed(self):  
    if self.__notify_id == 0:
      self.__notify_id = gobject.idle_add(self.__change_idle_cb)

  def __change_idle_cb(self):
    self.__notify_status_changed()
    self.__notify_id = 0
    
    if self.__callback:
      self.__callback()

    return False
  
  # make all entrys old
  def clean_keywords(self):
    pass

  # remove all entrys marked old
  def remove_old(self):
    pass
