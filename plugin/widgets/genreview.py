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

    self.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
    self.set_shadow_type(gtk.SHADOW_IN)

  def save_config(self):
    pass

  def load_config(self):
    pass