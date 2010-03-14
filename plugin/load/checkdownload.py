import os, shutil, time, sys, gobject

import rb

import debug

class CheckDownload:
  
  # dir where file placed
  file_dir = None 
  # local file name
  file_local = None
  # local temporary file name (temporary download location)
  file_local_temp = None
  # where to get this file from the internet
  file_url = None
  
  # 10 hours interval
  check_interval = 10 * 60 * 60

  file_check = None
  # indicate file completely downloaded
  has_loaded = False
  # xml file parser (parse and commit data to rhythmdb)
  catalogue_loader = None
  
  # download error state
  error = None
  
  __callback = None
  __notify_id = 0
  
  # parser/downloader status
  load_current_size = 0
  load_total_size = 0

  def __init__(self, file_local, file_url):
    self.file_dir = os.path.dirname(file_local)
    self.file_local = file_local
    self.file_local_temp = file_local + '.tmp'
    self.file_url = file_url
  
  # run update for local file
  def check_update(self):
    if self.ready_to_update():
      self.file_check = rb.UpdateCheck()
      self.file_check.check_for_update(self.file_local, self.file_url, self.update_cb)
      return True
    else:
      return False

  # get downloading in progress state
  def check_progress(self):
    if self.error:
      return False
    
    if self.catalogue_check:
      return True
    
    if self.catalogue_loader:
      return True

    return False
  
  # get downloading results: ok/error
  def check_result(self):
    return self.error
  
  # set callback for status notifications
  def check_callback(self, callback):
    self.__callback = callback

  def set_error(self, e):
    self.error = e

  def ready_to_update(self):
    try:
      (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(self.file_local)
      return mtime + self.check_interval < time.time()
    except OSError:
      return True

  def update_cb (self, result):
    try:
      self.catalogue_check = None
      if result is True:
        self.catalogue_download()
      else:
        self.set_error('error on update_cb')
    except:
      self.set_error(debug.fe())
      
    self.__notify_status_changed()

  def catalogue_download(self):
    if os.path.exists(self.file_dir) is False:
      os.mkdir(self.file_dir, 0700)

    debug.log(self.file_local_temp)
    out = open(self.file_local_temp, 'w')

    self.catalogue_loader = rb.ChunkLoader()
    self.catalogue_loader.get_url_chunks(self.file_url, 1 * 1024, True, self.catalogue_download_chunk_cb, out)

  def catalogue_download_chunk_close(self, out):
    self.catalogue_loader = None
    out.close()

  def catalogue_download_chunk_cb (self, result, total, out):
    try:
      if not result:
        self.catalogue_download_chunk_close(out)
        shutil.move(self.file_local_temp, self.file_local)
        debug.log(self.file_local)
      elif isinstance(result, Exception):
        self.catalogue_download_chunk_close(out)
        os.remove(self.file_local_temp)
        self.set_error(result)
      else:
        out.write(result)
        self.load_current_size += len(result)
        self.load_total_size = total
    except:
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
