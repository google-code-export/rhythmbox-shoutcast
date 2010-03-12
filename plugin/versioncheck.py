import os
import rhythmdb, rb
import time
import ConfigParser
import gobject
import shutil

class VersionCheck:
  
  file_url = 'http://wiki.rhythmbox-shoutcast.googlecode.com/hg/LastVersion.wiki'
  home_url = ''
  
  # if you feels paranoid you can diable version check for this plugin.
  # simple change DISABLE = True
  DISABLE = False

  # local file name
  file_local = None
  # local temporary file name (temporary download location)
  file_local_temp = None

  catalogue_loader = None
  rb_plugin = None
  notify_id = 0
  
  version = None
  
  def __init__(self, cache_dir, rb_plugin):
    self.file_dir = cache_dir
    self.file_local = os.path.join(cache_dir, 'versioncheck')
    self.file_local_temp = self.file_local + '.tmp'
    
    self.rb_plugin = rb_plugin
    
    config = ConfigParser.ConfigParser()
    config.read(self.rb_plugin)
    
    self.version = config.get('RB Plugin', 'Version', None)
    self.home_url = config.get('RB Plugin', 'Website', None)

  def check(self):
    if self.DISABLE:
      return
    
    if not self.ready_to_update():
      return
    
    self.version_download()

  def error(self, e):
    print e

  # do update each day only
  def ready_to_update(self):
    try:
      (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(self.file_local)
      return mtime + 24 * 60 * 60 < time.time()
    except:
      return True

  def version_download(self):
    self.updating = True
    
    if os.path.exists(self.file_dir) is False:
      os.mkdir(self.file_dir, 0700)

    print self.file_local_temp
    out = open(self.file_local_temp, 'w')

    self.version_loader = rb.ChunkLoader()
    self.version_loader.get_url_chunks(self.file_url, 1 * 1024, True, self.version_download_chunk_cb, out)

  def version_download_chunk_close(self, out):
    self.updating = False
    self.version_loader = None
    
    out.close()
    shutil.move(self.file_local_temp, self.file_local)
    print self.file_local

  def version_download_chunk_cb (self, result, total, out):
    try:
      if not result:
        self.version_download_chunk_close(out)
        self.version_load()
        
      elif isinstance(result, Exception):
        self.version_download_chunk_close(out)
        
        try:
          os.remove(self.file_local)
        except:
          pass
        
        self.error(result)
       
      else:
        out.write(result)
        self.load_current_size += len(result)
        self.load_total_size = total
        
    except Exception as e:
      
      try:
        os.remove(self.file_local)
      except:
        pass
      
      self.error(e)

    self.notify_status_changed()

  def version_load(self):
    file = open(self.file_local)
    version = file.readline()
    
    if self.version != version:
      self.notify(_("Rhythmbox-Shoutcast plugin"),
                  _("New version available: ") + version + _("\n\nPlease visit " + self.home_url));

  def notify(self, message, version):
    try:
        import pynotify
        if pynotify.init("Rhythmbox shoutcast plugin"):
            n = pynotify.Notification(message, version)
            n.show()
        else:
            raise "Unable to initialize pynotify"
    except e:
        print e

  def notify_status_changed(self):  
    if self.notify_id == 0:
      self.notify_id = gobject.idle_add(self.change_idle_cb)

  def change_idle_cb(self):
    self.notify_status_changed()
    self.notify_id = 0
      
    return False
  