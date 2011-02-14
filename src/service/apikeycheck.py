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
import os, time, ConfigParser, gobject, shutil
import load, debug

class ApikeyCheck(load.CheckDownload):
  
  # if you have you own key, or you made a fork please provide your own key, or disable check
  DISABLE = False
  
  apikey = None
  apiprivate = None
  
  def __init__(self, cache_dir):
    load.CheckDownload.__init__(self, os.path.join(cache_dir, 'apikey'),
                                'http://wiki.rhythmbox-shoutcast.googlecode.com/hg/SHOUTCastKey.wiki')

    self.apiprivate = self.file_local + '.private'

    self.check_interval = 24 * 60 * 60

    self.check_callback(self.check_status)

  def check(self):
    if self.DISABLE:
      return
    
    # do logic related to private (developers) shoutcast api keys
    if self.apikey_file_exist_f(self.apiprivate):
      self.apikey_load_f(self.apiprivate)
      return
    
    # if file need to be updated, do not load_key right now
    if self.check_update():
      return

    self.apikey_load()

  def check_status(self):
    if self.check_progress():
      return
    
    if self.check_result():
      self.load_failed()
      return
    
    self.apikey_load()

  def apikey_search(self, file):
    while file:
      line = file.readline()
      if not line:
        break;
      if not line.startswith('#') and len(line) > 0 and not line.isspace():
        return line
      
    raise Exception("Unable to find apikey in a file")

  def apikey_load_f(self, file):
    file = open(file)

    self.apikey = self.apikey_search(file)
    
    self.load_succesed()

  def apikey_load(self):
    self.apikey_load_f(self.file_local)

  def apikey_file_exist_f(self, file):
    try:
      (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(file)
      return True
    except OSError:
      return False

  def apikey_file_exist(self):
    return self.apikey_file_exist_f(self.file_local)

  # use self.check_result() to get an error text
  def load_failed(self):
    pass
  
  def load_succesed(self):
    pass