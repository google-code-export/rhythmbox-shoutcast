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

import rb, rhythmdb
import gobject, gconf, os, gtk, gettext, pango

class GenresView(rb.PropertyView):

  db = None
  prop = None
  name = None
  filter = False
  
  def __init__ (self, db, entry_type):
    rb.PropertyView.__init__(self, db, rhythmdb.PROP_GENRE, _("Genres"))

    self.db = db
    self.entry_type = entry_type
    self.gconf = gconf.client_get_default()

    self.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
    self.set_shadow_type(gtk.SHADOW_IN)
    
    cell_render = gtk.CellRendererText()
    column = gtk.TreeViewColumn()
    column.pack_start(cell_render)
    column.set_cell_data_func(cell_render, self.data_func)
    column.set_sizing (gtk.TREE_VIEW_COLUMN_FIXED)
    column.set_title (_("Genres"))
    self.append_column_custom(column)

  def data_func(self, column,renderer, tree_model, iter):
    (title, is_all, number) = tree_model.get(iter, rhythmdb.PROPERTY_MODEL_COLUMN_TITLE, rhythmdb.PROPERTY_MODEL_COLUMN_PRIORITY, rhythmdb.PROPERTY_MODEL_COLUMN_NUMBER)

    if is_all:
      nodes = tree_model.iter_n_children(None)
      nodes -= 1
      
      fmt = gettext.ngettext("%d genre (%d)", "All %d genres (%d)", nodes)
      str = fmt % (nodes, number)
    else:
      
      if not self.filter:
        number -= 1
        
      if number == 0:
        str = ("%s") % (title)
      else:
        str = ("%s (%d)") % (title, number)

    renderer.set_property('text', str)
    renderer.set_property('weight', is_all and pango.WEIGHT_BOLD or number == 0 and pango.WEIGHT_THIN or pango.WEIGHT_NORMAL)

  def do_query(self, filter):
    genres_query = self.db.query_new()
    self.db.query_append(genres_query, (rhythmdb.QUERY_PROP_EQUALS, rhythmdb.PROP_TYPE, self.entry_type))
    if filter:
      self.db.query_append(genres_query, (rhythmdb.QUERY_PROP_LIKE, rhythmdb.PROP_KEYWORD, 'star'))
    genres_query_model = self.db.query_model_new_empty ()
    self.db.do_full_query_parsed(genres_query_model, genres_query)
    self.get_model().set_property('query-model', genres_query_model)
    
    self.filter = filter

  def genre(self):
    genres = self.get_selection()
    
    if len(genres) > 0:
      return genres[0]
    else:
      return None

  def save_config(self):
    self.gconf.set_list('/apps/rhythmbox/plugins/shoutcast/genres_selection', 'string', self.get_selection())

  def load_config(self):
    self.set_selection(self.gconf.get_list('/apps/rhythmbox/plugins/shoutcast/genres_selection', 'string'))
