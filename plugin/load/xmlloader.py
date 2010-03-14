import rhythmdb
import xml.sax, xml.sax.handler
import shutil
import gobject
import rb
import os, time

from checkdownload import *

class XmlLoader(CheckDownload):

  db = None
  shell = None
  entry_type = None

  # xml hander for file_local file
  xml_handler = None

  fresh = True
    
  # exception / error text message
  error = None
  
  __callback = None
  __notify_id = 0
  
  def __init__(self, file, url):
    CheckDownload.__init__(self, file, url)
    
    self.check_callback(self.download_state)
  
  def loader_progress(self):
    if self.error:
      return False
   
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
    self.catalogue_loader.get_url_chunks(self.file_local, 1 * 1024, True, self.catalogue_load_chunk_cb, parser)

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

        self.load_current_size += len(result)
        self.load_total_size = total
    except SAXParseException:
      if self.catalogue_loader:
        self.catalogue_loader.cancel()
      self.close_and_remove()
      self.set_error(debug.fe())
    except:
      if self.catalogue_loader:
        self.catalogue_loader.cancel()
      self.set_error(debug.fe())

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
