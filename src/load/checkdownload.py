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

import os, shutil, time, sys, gobject
import rb
import debug, service

class CheckDownload:
  
  # dir where file placed
  file_dir = None 
  # local file name
  file_local = None
  # local temporary file name (temporary download location)
  file_local_temp = None
  # where to get this file from the internet
  file_url = None
  
  # 24 hours interval
  check_interval = 24 * 60 * 60

  __file_check = None
  # xml file parser (parse and commit data to rhythmdb)
  __catalogue_loader = None

  # download error state
  __error = None
  
  __callback = None
  __notify_id = 0
  
  # parser/downloader status
  __load_current_size = 0
  __load_total_size = 0

  def __init__(self, file_local, file_url):
    self.file_dir = os.path.dirname(file_local)
    self.file_local = file_local
    self.file_local_temp = file_local + '.tmp'
    self.file_url = file_url
  
  # run update for local file, return Ture if file need to be downloaded
  def check_update(self):
    if self.ready_to_update():
      self.__file_check = rb.UpdateCheck()
      self.__file_check.check_for_update(self.file_local, self.file_url, self.update_cb)
      return True
    else:
      return False

  # get downloading in progress state
  def check_progress(self):
    if self.__error:
      return False
    
    if self.__file_check:
      return True
    
    if self.__catalogue_loader:
      return True

    return False
  
  # get downloading results: ok/error
  def check_result(self):
    return self.__error
  
  # set callback for status notifications
  def check_callback(self, callback):
    self.__callback = callback
    
  def check_get_progress(self):
    if self.__load_total_size != 0:
      return (self.file_url, self.__load_current_size / float(self.__load_total_size))
    else:
      return (self.file_url, -1)

  def check_remove_target(self):
    try:
      os.remove(self.file_local)
    except OSError:
      pass

  def set_error(self, e):
    self.__error = e

  # return true if local file is outdate (self.check_interval variable), or absent
  def ready_to_update(self):
    try:
      (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(self.file_local)
      return mtime + self.check_interval < time.time()
    except OSError:
      return True

  def update_cb (self, result):
    try:
      self.__file_check = None
      if result is True:
        self.catalogue_download()
      else:
        self.set_error('error on update_cb')
    except:
      self.set_error(service.fe())
      
    self.__notify_status_changed()

  def catalogue_download(self):
    if os.path.exists(self.file_dir) is False:
      os.mkdir(self.file_dir, 0700)

    debug.log(self.file_local_temp)
    out = open(self.file_local_temp, 'w')

    self.__catalogue_loader = rb.ChunkLoader()
    self.__catalogue_loader.get_url_chunks(self.file_url, 1 * 1024, True, self.catalogue_download_chunk_cb, out)

  def catalogue_download_chunk_close(self, out):
    self.__catalogue_loader = None
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
        self.__load_current_size += len(result)
        self.__load_total_size = total
    except:
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
