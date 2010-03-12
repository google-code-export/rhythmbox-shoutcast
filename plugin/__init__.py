import rhythmdb, rb
import gobject
import gtk
import gconf, gnome

import urllib
import zipfile
import sys, os.path
import xml
import datetime
import string

from shoutcastsource import *
from versioncheck import *

class Shoutcast(rb.Plugin):

  client = None
  
  cache_dir = None
	
  versioncheck = None
  
  source = None

  def __init__(self):
    rb.Plugin.__init__(self)

    self.client = gconf.client_get_default()

  def activate(self, shell):
    self.shell = shell
    self.db = self.shell.props.db

    self.cache_dir = os.path.join(rb.user_cache_dir(), 'shoutcast')
    
    self.versioncheck = VersionCheck(self.cache_dir, self.find_file("shoutcast.rb-plugin"))    
    self.versioncheck.check()

    group = rb.rb_source_group_get_by_name ("library")

    self.entry_type = self.db.entry_register_type("ShoutcastEntryType")
    self.entry_type.can_sync_metadata = True
    self.entry_type.sync_metadata = None
    self.entry_type.save_to_disk = True
    self.entry_type.category = rhythmdb.ENTRY_STREAM

    width, height = gtk.icon_size_lookup(gtk.ICON_SIZE_LARGE_TOOLBAR)
    icon = gtk.gdk.pixbuf_new_from_file_at_size(self.find_file("shoutcast.png"), width, height)

    self.source = gobject.new(ShoutcastSource,
           					   shell = self.shell,
           					   plugin = self,
                       icon = icon,
                       entry_type = self.entry_type,
                       source_group = group,
                       cache_dir = self.cache_dir)

    shell.register_entry_type_for_source(self.source, self.entry_type)
    shell.append_source(self.source, None)

    #self.manager = shell.get_player().get_property('ui-manager')
    #self.manager.ensure_update()

  def deactivate(self, shell):
    self.db = None
    self.entry_type_g = None
    self.entry_type_s = None
    self.source.delete_thyself()
    self.source = None
    self.shell = None

  def create_configure_dialog(self, dialog):
    pass
