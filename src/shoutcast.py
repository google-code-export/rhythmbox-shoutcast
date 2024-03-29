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
import gobject, gtk, gconf, urllib, zipfile, sys, os.path, xml, datetime, string
import service, rbdb

from shoutcastsource import *

class Shoutcast(rb.Plugin):

  cache_dir = None
  versioncheck = None
  source = None

  def __init__(self):
    rb.Plugin.__init__(self)

  def activate(self, shell):
    self.shell = shell
    self.db = self.shell.props.db

    self.data_dir = os.path.join(rb.user_data_dir(), 'shoutcast')
    self.cache_dir = os.path.join(rb.user_cache_dir(), 'shoutcast')
    
    self.versioncheck = service.VersionCheck(self.cache_dir, self.find_file("shoutcast.rb-plugin"))    
    self.versioncheck.check()

    self.entry_type = rbdb.register_entry_type(self.db, 'ShoutcastEntryType')

    width, height = gtk.icon_size_lookup(gtk.ICON_SIZE_LARGE_TOOLBAR)
    icon = gtk.gdk.pixbuf_new_from_file_at_size(self.find_file("shoutcast.png"), width, height)

    # rhythmbox api break up (0.13.2 - 0.13.3)
    if hasattr(rb, 'rb_source_group_get_by_name'):
      group = rb.rb_source_group_get_by_name ("library")

      if not group:
        group = rb.rb_source_group_register ("library",
                                             _("Library"),
                                             rb.SOURCE_GROUP_CATEGORY_FIXED)
      
      self.source = gobject.new(ShoutcastSource,
                          shell = self.shell,
                          plugin = self,
                          icon = icon,
                          entry_type = self.entry_type,
                          source_group = group,
                          cache_dir = self.cache_dir,
                          data_dir = self.data_dir)
      
      shell.register_entry_type_for_source(self.source, self.entry_type)
      shell.append_source(self.source, None)
    else:
      group = rb.rb_display_page_group_get_by_id ("library")

      self.source = gobject.new(ShoutcastSource,
                          shell = self.shell,
                          plugin = self,
                          pixbuf = icon,
                          entry_type = self.entry_type,
                          cache_dir = self.cache_dir,
                          data_dir = self.data_dir)
        
      shell.register_entry_type_for_source(self.source, self.entry_type)
      shell.append_display_page(self.source, group)
    
    # hack, should be done within gobject constructor
    self.source.init()

  def deactivate(self, shell):
    self.db = None
    self.entry_type = None
    self.source.delete_thyself()
    self.source = None
    self.shell = None

#  def create_configure_dialog(self):
#    pass
