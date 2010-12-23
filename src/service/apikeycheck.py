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
  
  def __init__(self, cache_dir, rb_plugin):
    load.CheckDownload.__init__(self, os.path.join(cache_dir, 'apikey'),
                                'http://wiki.rhythmbox-shoutcast.googlecode.com/hg/SHOUTCastKey.wiki')

    self.check_interval = 24 * 60 * 60

    self.rb_plugin = rb_plugin
        
    self.check_callback(self.check_status)

  def check(self):
    if self.DISABLE:
      return
    
    if self.check_update():
      return

    self.apikey_load()

  def check_status(self):
    if self.check_progress():
      return
    
    if self.check_result():
      debug.log(self.check_result())
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

  def apikey_load(self):
    file = open(self.file_local)

    apikey = self.apikey_search(file)
    
    description = ''.join(file.readlines()).strip()
    
    description = description.strip('{{{')
    description = description.strip('}}}')
    description = description.strip()
    
    self.rb_plugin.set_apikey(apikey)