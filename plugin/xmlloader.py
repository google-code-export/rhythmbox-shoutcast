import rhythmdb
import xml.sax, xml.sax.handler
import shutil
import gobject
import rb
import os

class XmlLoader:

  db = None
  shell = None
  entry_type = None
  
  # dir where file placed
  file_dir = None 
  # local file name
  file_local = None
  # local temporary file name (temporary download location)
  file_local_temp = None
  # where to get this file from the internet
  file_url = None
  
  # xml hander for file_local file
  xml_handler = None
  
  update_id = None
  # rb.UpdateCheck() comparator
  catalogue_check = None
  # indicate file completely downloaded
  has_loaded = False
  # xml file parser (parse and commit data to rhythmdb)
  catalogue_loader = None
  # finally flag (everything done) None/False/True
  updating = None
  
  # parser/downloader status
  load_current_size = 0
  load_total_size = 0
  
  # gtk id
  notify_id = 0
  
  def __init__(self):
    pass
  
  def update(self):
    self.clean_keywords()
    self.update_id = gobject.timeout_add(6 * 60 * 60 * 1000, self.update_catalogue)
    self.update_catalogue()

  def update_catalogue(self):
    self.catalogue_check = rb.UpdateCheck()
    self.catalogue_check.check_for_update(self.file_local, self.file_url, self.update_cb)

  def update_cb (self, result):
      self.catalogue_check = None
      if result is True:
        self.catalogue_download()
      elif self.has_loaded is False:
        self.catalogue_load()

  def catalogue_download(self):
    self.updating = True
    
    if os.path.exists(self.file_dir) is False:
      os.mkdir(self.file_dir, 0700)
      
    out = open(self.file_local_temp, 'w')

    self.catalogue_loader = rb.ChunkLoader()
    self.catalogue_loader.get_url_chunks(self.file_url, 4*1024, True, self.catalogue_download_chunk_cb, out)

  def catalogue_download_chunk_cb (self, result, total, out):
    if not result:
      out.close()

      shutil.move(self.file_local_temp, self.file_local)
      self.updating = False
      self.catalogue_loader = None
      self.catalogue_load()
    elif isinstance(result, Exception):
      pass
    else:
      out.write(result)
      self.load_current_size += len(result)
      self.load_total_size = total

    self.notify_status_changed()

  def catalogue_load(self):
    self.notify_status_changed()
    self.has_loaded = True

    parser = xml.sax.make_parser()
    parser.setContentHandler(self.xml_handler)
    
    self.catalogue_loader = rb.ChunkLoader()
    self.catalogue_loader.get_url_chunks(self.file_local, 64*1024, True, self.catalogue_load_chunk_cb, parser)

  def catalogue_load_chunk_cb(self, result, total, parser):
    if not result or isinstance (result, Exception):
      parser.close ()
      
      self.updating = False
      self.catalogue_loader = None
      
      self.remove_old();
    else:
      print result
      parser.feed(result)
      
      self.load_current_size += len(result)
      self.load_total_size = total

    self.notify_status_changed()

  def notify_status_changed(self):  
    if self.notify_id == 0:
      self.notify_id = gobject.idle_add(self.change_idle_cb)

  def change_idle_cb(self):
    self.notify_status_changed()
    self.notify_id = 0
    return False

  #
  # i have problems with deleting entries when i ran entry_foreach_by_type.
  # probably entry_foreach_by_type has side effect like std::vector//std::list in stl
  
  def clean_keywords(self):
    #self.db.entry_foreach_by_type(self.entry_type, self.clean_keywords_db)
    self.db.entry_delete_by_type(self.entry_type)

  def clean_keywords_db(self, entry):
    self.db.entry_keyword_remove(entry, 'new')

  def remove_old(self):
    #self.db.entry_foreach_by_type(self.entry_type, self.remove_old_db)
    pass
    
  def remove_old_db(self, entry):
    if self.db.entry_keyword_has(entry, 'new') == False:
      self.db.entry_delete(entry)
