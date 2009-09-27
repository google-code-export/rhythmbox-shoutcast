import rb, rhythmdb
import gobject
import os
import gtk

from xmlgenreloader import XmlGenreLoader

class ShoutcastSource(rb.Source):

  __gproperties__ = {
                     'plugin': (rb.Plugin, 'plugin', 'plugin', gobject.PARAM_READABLE | gobject.PARAM_CONSTRUCT_ONLY),
                     'entry_type_g': (rhythmdb.EntryType, 'entry_type_g', 'entry_type_g', gobject.PARAM_READABLE | gobject.PARAM_CONSTRUCT_ONLY),
  }
  
  db = None
  shell = None
  entry_type_s = None
  entry_type_g = None
  cache_dir = None
  plugin = None
  
  genresloader = None
  
  activated = False
  
  def __init__ (self):
    rb.Source.__init__(self, name=_("Shoutcast"))
    
    self.cache_dir = os.path.join(rb.user_cache_dir(), 'shoutcast')

  def do_set_property(self, property, value):
    if property.name == 'plugin':
      self.plugin = value
    elif property.name == 'entry_type_g':
      self.entry_type_g = value
    else:
      raise AttributeError, 'unknown property %s' % property.name

    def create(self, shell, entry_type_s, entry_type_g, plugin):
      self.shell = shell
      self.db = self.shell.props.db
      
      self.entry_type_s = entry_type_s
  
      self.entry_type_g = entry_type_g
  
      self.plugin = plugin

  def do_impl_activate(self):
    if not self.activated:
      self.activated = True

      self.genresloader = XmlGenreLoader(self.db, self.cache_dir, self.entry_type_s)

      self.builder = gtk.Builder()
      self.builder.add_from_file(os.path.join(self.plugin.find_file("shoutcast.glade")))

      self.add(self.builder.get_object('scrolledwindow1'))

    rb.Source.do_impl_activate (self)

gobject.type_register(ShoutcastSource)
