import rhythmdb
import xml.sax, xml.sax.handler
import shutil

class XmlGenreLoader:

  db = None
  shell = None
  entry_type = None
  
  file_local = None
  file_local_temp = None
  file_url = None
  
  def __init__(self):
    self.file_local = os.path.join(cache_dir, 'genres.xml')
    self.file_local_temp = os.path.join(self.file_local, '.tmp')
    self.file_url = 'http://yp.shoutcast.com/sbin/newxml.phtml'

  def update(self):
    self.update_id = gobject.timeout_add(6 * 60 * 60 * 1000, self.update_catalogue)
    self.update_catalogue()

  def update_catalogue(self):
    self.catalogue_check = rb.UpdateCheck()
    self.catalogue_check.check_for_update(file_local, file_url, update_cb)

  def update_cb (result):
      self.catalogue_check = None
      if result is True:
        self.catalogue_download()
      elif self.has_loaded is False:
        self.catalogue_load()

  def catalogue_load(self):
    self.notify_status_changed()
    self.has_loaded = True

    parser = xml.sax.make_parser()
    parser.setContentHandler(XmlGenreHandler(self.db, self.entry_type))
    
    self.catalogue_loader = rb.ChunkLoader()
    self.catalogue_loader.get_url_chunks(file_local, 64*1024, True, self.catalogue_load_chunk_cb, parser)

  def catalogue_load_chunk_cb(self, result, total, parser):
    if not result or isinstance (result, Exception):
      parser.close ()

      self.updating = False
      self.catalogue_loader = None
    else:
      parser.feed(result)

      self.load_current_size += len(result)
      self.load_total_size = total

    self.notify_status_changed()

  def catalogue_download(self):
    self.updating = True
    
    out = open(file_local_temp, 'w')

    self.catalogue_loader = rb.ChunkLoader()
    self.catalogue_loader.get_url_chunks(file_url, 4*1024, True, self.catalogue_download_chunk_cb, out)

    
  def catalogue_download_chunk_cb (self, result, total, out):
    if not result:
      out.close()

      shutil.move(file_local_temp, file_local)
      self.updating = False
      self.catalogue_loader = None
      self.load_catalogue()

    elif isinstance(result, Exception):
      pass
    else:
      out.write(result)
      self.load_current_size += len(result)
      self.load_total_size = total

    self.notify_status_changed()

  def notify_status_changed(self):  
    if self.notify_id == 0:
      self.notify_id = gobject.idle_add(change_idle_cb)

  def change_idle_cb():
    self.notify_status_changed()
    self.notify_id = 0
    return False
