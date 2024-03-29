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

class VersionCheck(load.CheckDownload):
  
  # if you feels paranoid you can diable version check for this plugin.
  # it is simple, just change DISABLE = True
  DISABLE = False

  rb_plugin = None  
  version = None
  
  def __init__(self, cache_dir, rb_plugin):
    load.CheckDownload.__init__(self, os.path.join(cache_dir, 'versioncheck'),
                                'http://wiki.rhythmbox-shoutcast.googlecode.com/git/LastVersion170.wiki')

    self.check_interval = 24 * 60 * 60

    self.rb_plugin = rb_plugin
    
    config = ConfigParser.ConfigParser()
    config.read(self.rb_plugin)
    
    self.version = config.get('RB Plugin', 'Version', None)
    self.home_url = config.get('RB Plugin', 'Website', None)
    
    self.check_callback(self.check_status)

  def check(self):
    if self.DISABLE:
      return
    
    if self.check_update():
      return

    self.version_load()

  def check_status(self):
    if self.check_progress():
      return
    
    if self.check_result():
      debug.log(self.check_result())
      return
    
    self.version_load()

  def version_search(self, file):
    while file:
      line = file.readline()
      if not line:
        break;
      if not line.startswith('#') and len(line) > 0 and not line.isspace():
        return line
      
    raise Exception("Unable to find version in a file")

  def version_load(self):
    file = open(self.file_local)

    version = self.version_search(file)
    
    description = ''.join(file.readlines()).strip()
    
    description = description.strip('{{{')
    description = description.strip('}}}')
    description = description.strip()
    
    vs_site = version.split('.')
    vs_local = self.version.split('.')
    
    for i in range(3):
      if int(vs_local[i]) < int(vs_site[i]):
        self.notify(_("Rhythmbox-SHOUTcast plugin"),
                    _("New version available: ") + version +
                    '\n\n' + description + _("\n\nPlease visit " + self.home_url));
        break
      elif int(vs_local[i]) > int(vs_site[i]):
        break

  def notify(self, message, version):
    try:
        import pynotify
        if pynotify.init("Rhythmbox SHOUTcast plugin"):
            n = pynotify.Notification(message, version)
            n.show()
        else:
            raise Exception("Unable to initialize pynotify")
    except e:
        self.error(e)
