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
import gobject, gconf, gnome, os, gtk

class GenresView(rb.PropertyView):

  db = None
  prop = None
  name = None
  
  def __init__ (self, db, prop, name):
    rb.PropertyView.__init__(self, db, prop, name)

    self.db = db
    self.prop = prop
    self.name = name
    self.gconf = gconf.client_get_default()

    self.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
    self.set_shadow_type(gtk.SHADOW_IN)

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
