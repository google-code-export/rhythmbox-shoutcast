import rhythmdb
import xml.sax, xml.sax.handler
import shutil
import gobject
import rb
import os, time

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
  
  # exception / error text message
  result = None
  
  callback = None
  
  def __init__(self):
    pass
  
  def iter_to_entry(self, model, iter):
    id = model.get(iter, 0)[0]
    return self.db.entry_lookup_by_id(self.db.entry_get (id, rhythmdb.PROP_ENTRY_ID))

  def entry_to_string(self, entry):
    print "id: " + repr(self.db.entry_get(entry, rhythmdb.PROP_ENTRY_ID))
    print "title: " + repr(self.db.entry_get(entry, rhythmdb.PROP_TITLE))
    print "genre: " + repr(self.db.entry_get(entry, rhythmdb.PROP_GENRE))
    print "url: " + repr(self.db.entry_get(entry, rhythmdb.PROP_LOCATION))

  def set_callback(self, callback):
    self.callback = callback
  
  def fresh(self):
    return self.update_id == None
  
  def done(self):
    if self.result:
      return True
    
    if self.catalogue_check:
      return False
    
    if self.catalogue_loader:
      return False
    
    return True
  
  # do update each 10 min only
  def ready_to_update(self):
    try:
      (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(self.file_local)
      return mtime + 10 * 60 * 60 < time.time()
    except OSError:
      return True

  def error(self, result):
    print result
    self.result = result
  
  def update(self):    
    self.clean_keywords()
    self.update_id = gobject.timeout_add(6 * 60 * 60 * 1000, self.update_catalogue)
    self.update_catalogue()

  def update_catalogue(self):
    if self.ready_to_update():
      self.catalogue_check = rb.UpdateCheck()
      self.catalogue_check.check_for_update(self.file_local, self.file_url, self.update_cb)
    else:
      self.catalogue_load()

  def update_cb (self, result):
    try:
      self.catalogue_check = None
      
      if result is True:
    	  self.catalogue_download()
      elif self.has_loaded is False:
        self.catalogue_load()
      else:
        self.error('update')
    except Exception as e:
      self.error(e)

  def catalogue_download(self):
    self.updating = True
    
    if os.path.exists(self.file_dir) is False:
      os.mkdir(self.file_dir, 0700)
      
    print self.file_local_temp
    out = open(self.file_local_temp, 'w')

    self.catalogue_loader = rb.ChunkLoader()
    self.catalogue_loader.get_url_chunks(self.file_url, 4 * 1024, True, self.catalogue_download_chunk_cb, out)

  def catalogue_download_chunk_close(self, out):
    self.updating = False
    self.catalogue_loader = None
    
    out.close()
    shutil.move(self.file_local_temp, self.file_local)
    print self.file_local

  def catalogue_download_chunk_cb (self, result, total, out):
    try:
      if not result:
        self.catalogue_download_chunk_close(out)
        self.catalogue_load()
        
      elif isinstance(result, Exception):
        self.catalogue_download_chunk_close(out)
        os.remove(self.file_local)
        self.error(result)
       
      else:
        out.write(result)
        self.load_current_size += len(result)
        self.load_total_size = total
    except Exception as e:
      self.error(e)

    self.notify_status_changed()

  def catalogue_load(self):
    self.notify_status_changed()
    self.has_loaded = True

    parser = xml.sax.make_parser()
    parser.setContentHandler(self.xml_handler)
    
    self.catalogue_loader = rb.ChunkLoader()
    self.catalogue_loader.get_url_chunks(self.file_local, 64 * 1024, True, self.catalogue_load_chunk_cb, parser)

  def catalogue_load_chunk_close(self, parser):
    parser.close()
    
    self.updating = False
    self.catalogue_loader = None
    
    self.db.commit()
    
    self.remove_old()

  def catalogue_load_chunk_cb(self, result, total, parser):
    try:
      if not result:
        self.catalogue_load_chunk_close(parser)
              
      elif isinstance(result, Exception):
        self.error(result)
        self.catalogue_load_chunk_close(parser)
        
      else:
        parser.feed(result)
        
        self.load_current_size += len(result)
        self.load_total_size = total
    except Exception as e:
      self.error(e)

    self.notify_status_changed()

  def notify_status_changed(self):  
    if self.notify_id == 0:
      self.notify_id = gobject.idle_add(self.change_idle_cb)

  def change_idle_cb(self):
    self.notify_status_changed()
    self.notify_id = 0
    
    if self.callback:
      self.callback()
      
    return False
  
  # make all entrys old
  def clean_keywords(self):
    pass

  # remove all entrys marked old
  def remove_old(self):
    pass
