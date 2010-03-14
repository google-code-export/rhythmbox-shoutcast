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

import rb
import gtk, gconf, gnome
import debug

from db import *
from cellpixbufbutton import *

class EntryView(rb.EntryView):

  plugin = None
  pixs = []

  def __init__(self, db, player, plugin):
    rb.EntryView.__init__(self,db, player, None, False, False)
    
    self.db = db
    self.plugin = plugin
    self.gconf = gconf.client_get_default()
    
    self.pixs = [gtk.gdk.pixbuf_new_from_file(self.plugin.find_file('widgets/star-off.png')),
                 gtk.gdk.pixbuf_new_from_file(self.plugin.find_file('widgets/star-on.png'))]

    self.append_column(rb.ENTRY_VIEW_COL_TITLE, True)

    cell_render = CellPixbufButton()
    cell_render.connect('toggled', self.star_click)
    column = gtk.TreeViewColumn()
    column.pack_start(cell_render)
    column.set_cell_data_func(cell_render, self.star_func)
    column.set_sizing (gtk.TREE_VIEW_COLUMN_FIXED)
    #column.set_fixed_width(self.pixs[0].get_width())
    column.set_fixed_width(50)
    self.append_column_custom(column, "", "STAR")

    self.set_columns_clickable(False)
    self.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
    self.set_shadow_type(gtk.SHADOW_IN)

  def star_func(self, column, cell, model, iter):
    entry = iter_to_entry(self.db, model, iter)
    star = self.db.entry_keyword_has(entry, 'star')

    if star:
      pixbuf = self.pixs[1]
    else:
      pixbuf = self.pixs[0]

    cell.set_property('pixbuf', pixbuf)

  def star_click(self, cell, model, path, iter):
    entry = iter_to_entry(self.db, model, iter)
    
    star = self.db.entry_keyword_has(entry, 'star')
    if star:
      self.db.entry_keyword_remove(entry, 'star')
    else:
      self.db.entry_keyword_add(entry, 'star')

    self.db.commit()
    
    model.row_changed(path, iter)

  def get_entry_url(self):
    entrys = self.get_selected_entries()
    if len(entrys) > 0:
      entry = entrys[0]
      return self.db.entry_get(entry, rhythmdb.PROP_LOCATION)
    else:
      return None

  def save_config(self):
    self.gconf.set_string('/apps/rhythmbox/plugins/shoutcast/stations_entry', self.get_entry_url())

  def load_config(self):
    url = self.gconf.get_string('/apps/rhythmbox/plugins/shoutcast/stations_entry')
    if url:
      entry = self.db.entry_lookup_by_location(url)
      self.select_entry(entry)
      # hack
      gobject.idle_add(self.hack_scroll_to_entry, entry)
  
  def hack_scroll_to_entry(self, entry):
    self.scroll_to_entry(entry)
