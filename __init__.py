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

from shoutcastsource import ShoutcastSource

class Shoutcast(rb.Plugin):

  client = None
	
  def __init__(self):
    rb.Plugin.__init__(self)

    self.client = gconf.client_get_default()

  def activate(self, shell):
    self.shell = shell
    self.db = self.shell.props.db

    group = rb.rb_source_group_get_by_name ("library")

    self.entry_type_g = self.db.entry_register_type("ShoutcastGenresEntryType")
    self.entry_type_g.can_sync_metadata = True
    self.entry_type_g.sync_metadata = None
    self.entry_type_g.save_to_disk = True
    self.entry_type_g.category = rhythmdb.ENTRY_CONTAINER
    
    self.entry_type_s = self.db.entry_register_type("ShoutcastStationsEntryType")
    self.entry_type_s.can_sync_metadata = True
    self.entry_type_s.sync_metadata = None
    self.entry_type_s.save_to_disk = True
    self.entry_type_s.category = rhythmdb.ENTRY_CONTAINER
    
    theme = gtk.icon_theme_get_default()
    rb.append_plugin_source_path(theme, "/icons")

    width, height = gtk.icon_size_lookup(gtk.ICON_SIZE_LARGE_TOOLBAR)
    icon = rb.try_load_icon(theme, "shoutcast", width, 0)

    self.source = gobject.new (ShoutcastSource,
                   					   shell = self.shell,
                   					   plugin = self,
                               entry_type = self.entry_type_s,
                               entry_type_g = self.entry_type_g,
                               source_group = group)

    shell.register_entry_type_for_source(self.source, self.entry_type_s)
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
