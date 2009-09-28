import rb, rhythmdb
import gobject
import os
import gtk

from xmlgenresloader import XmlGenresLoader
from xmlstationsloader import XmlStationsLoader

class ShoutcastSource(rb.Source):

  __gproperties__ = {
                     'plugin': (rb.Plugin, 'plugin', 'plugin', gobject.PARAM_WRITABLE | gobject.PARAM_CONSTRUCT_ONLY),
                     'entry_type_g': (rhythmdb.EntryType, 'entry_type_g', 'entry_type_g', gobject.PARAM_WRITABLE | gobject.PARAM_CONSTRUCT_ONLY),
  }
  
  db = None
  shell = None
  entry_type_s = None
  entry_type_g = None
  cache_dir = None
  plugin = None
  
  genresloader = None
  stationsloader = None
  
  activated = False
  
  def __init__ (self):
    rb.Source.__init__(self, name=_("Shoutcast"))
    
    self.cache_dir = os.path.join(rb.user_cache_dir(), 'shoutcast')

  def do_set_property(self, property, value):
    if property.name == 'plugin':
      self.plugin = value
    elif property.name == 'entry-type-g':
      self.entry_type_g = value
    else:
      raise AttributeError, 'unknown property %s' % property.name

  def create(self):
      self.shell = self.get_property('shell')
      self.db = self.shell.props.db

      self.entry_type_s = self.get_property('entry-type')

      self.builder = gtk.Builder()
      self.builder.add_from_file(os.path.join(self.plugin.find_file('shoutcast.glade')))

      self.genres_list = rb.PropertyView(self.db, rhythmdb.PROP_GENRE, _("Genres"))
      self.filter_all_genres()
      #self.genres_list.connect('entry-activated')
      self.genres_list.connect('property-selected', self.genres_property_selected)
      self.genres_list.connect('property-selection-reset', self.genres_property_selection_reset)
      self.genres_list.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
      self.genres_list.set_shadow_type(gtk.SHADOW_IN)
      
      self.stations_list = rb.EntryView(self.db, self.shell.get_player(), None, False, False)
      self.stations_list.append_column(rb.ENTRY_VIEW_COL_TITLE, True)
      self.stations_list.set_columns_clickable(False)
      self.stations_list.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
      self.stations_list.set_shadow_type(gtk.SHADOW_IN)

      self.builder.get_object('vbox2').pack_start(self.genres_list)
      self.builder.get_object('vbox3').pack_start(self.stations_list)

      main_vbox = self.builder.get_object('main_vbox')
      main_vbox.show_all()

      self.add(main_vbox)

      self.genresloader = XmlGenresLoader(self.db, self.cache_dir, self.entry_type_s)
      self.genresloader.update()

  def filter_all_genres(self):
      genres_query = self.db.query_new()
      self.db.query_append(genres_query, (rhythmdb.QUERY_PROP_EQUALS, rhythmdb.PROP_TYPE, self.entry_type_s))
      genres_query_model = self.db.query_model_new_empty ()
      self.db.do_full_query_parsed(genres_query_model, genres_query)
      genres_props_model = self.genres_list.get_model()
      genres_props_model.set_property('query-model', genres_query_model)


  def filter_by_genre_clear(self):
      self.stations_query = self.db.query_new()
      self.stations_query_model = self.db.query_model_new_empty ()
      self.stations_list.set_model(self.stations_query_model)

  def filter_by_genre(self, genre):
      self.stations_query = self.db.query_new()
      self.db.query_append(self.stations_query, (rhythmdb.QUERY_PROP_EQUALS, rhythmdb.PROP_TYPE, self.entry_type_g))
      self.db.query_append(self.stations_query, (rhythmdb.QUERY_PROP_EQUALS, rhythmdb.PROP_GENRE, genre))
      self.stations_query_model = self.db.query_model_new_empty ()
      self.db.do_full_query_parsed(self.stations_query_model, self.stations_query)
      self.stations_list.set_model(self.stations_query_model)

      self.stationsloader = XmlStationsLoader(self.db, self.cache_dir, self.entry_type_g, genre)
      self.stationsloader.update()

  def genres_property_selected(self, view, name):
    ens = self.genres_list.get_selection()
    if not ens:
      self.filter_by_genre_clear()
    else:
      self.filter_by_genre(ens[0])

  def genres_property_selection_reset(self):
    self.filter_by_genre_clear()

  def do_impl_activate(self):
    if not self.activated:
      self.activated = True
      self.create()

    rb.Source.do_impl_activate (self)

gobject.type_register(ShoutcastSource)
