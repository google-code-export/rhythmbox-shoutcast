import rhythmdb, rb

import os, time, ConfigParser, gobject, shutil

import load, debug

class VersionCheck(load.CheckDownload):
  
  # if you feels paranoid you can diable version check for this plugin.
  # simple change DISABLE = True
  DISABLE = False

  rb_plugin = None  
  version = None
  
  def __init__(self, cache_dir, rb_plugin):
    load.CheckDownload.__init__(self, os.path.join(cache_dir, 'versioncheck'),
                                'http://wiki.rhythmbox-shoutcast.googlecode.com/hg/LastVersion.wiki')

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

  def version_load(self):
    file = open(self.file_local)
    version = file.readline()
    
    vs_site = version.split('.')
    vs_local = self.version.split('.')
    
    for i in range(3):
      if int(vs_local[i]) < int(vs_site[i]):
        self.notify(_("Rhythmbox-Shoutcast plugin"),
                    _("New version available: ") + version + _("\n\nPlease visit " + self.home_url));
        break

  def notify(self, message, version):
    try:
        import pynotify
        if pynotify.init("Rhythmbox shoutcast plugin"):
            n = pynotify.Notification(message, version)
            n.show()
        else:
            raise "Unable to initialize pynotify"
    except e:
        self.error(e)
