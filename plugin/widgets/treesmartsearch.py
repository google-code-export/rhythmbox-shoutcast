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

import rhythmdb
import gtk
import rbdb

class TreeSmartSearch:
  
  # GtkTreeView
  treeview = None
  # GtkTreeModelFilter
  treeviewmodel = None
  searchentry = None
  
  def __init__(self, db):
    self.db = db
  
  def catch_treecontrol(self, widget):
    if isinstance(widget, gtk.TreeView):
      self.treeview = widget
  
  def connect_to_tree(self, container, searchentry):
    self.container = container
    
    container.foreach(self.catch_treecontrol)
    
    if not self.treeview:
      raise Exception('Unable to find treeview')
    
    self.create()
    
    self.searchentry = searchentry
    self.searchentry.set_callback(self.new_filter_text)
    self.searchentry.set_focus_back(self.treeview)
    
  def create(self):
    self.treeview.set_property('enable-search', False)
    self.treeview.connect('key-press-event', self.keyboard_event)
    
  def keyboard_event(self, treeview, event):
    if self.searchentry.scope_event(event):
      self.searchentry.show_entry(event)
      return True
    
    if event.keyval == gtk.keysyms.Escape:
      self.searchentry.hide_entry()
      return True
  
  def set_model(self, model):
    self.searchentry.hide_entry()
    
    self.model = model
    self.treeviewmodel = self.db.query_model_new_empty()
    query = self.db.query_new()
    self.treeviewmodel.set_query(query)
    self.treeviewmodel.set_property('base-model', self.model)

  def filter_model(self, model):
    self.set_model(model)
    return self.treeviewmodel

  def new_filter_text(self, text):
    query = self.db.query_new()
    self.db.query_append(query, (rhythmdb.QUERY_PROP_LIKE, rhythmdb.PROP_TITLE, text))
    self.treeviewmodel.set_query(query)
    self.treeviewmodel.set_property('base-model', self.model)
    self.treeviewmodel.reapply_query(True)
    
    url = self.container.get_entry_url()
    if url:
      entry = self.db.entry_lookup_by_location(url)
      if entry:
        self.container.scroll_to_entry(entry)
