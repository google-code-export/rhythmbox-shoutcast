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

  def save_config(self):
    self.gconf.set_list('/apps/rhythmbox/plugins/shoutcast/genres_selection', 'string', self.get_selection())

  def load_config(self):
    self.set_selection(self.gconf.get_list('/apps/rhythmbox/plugins/shoutcast/genres_selection', 'string'))
