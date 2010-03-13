import rb, rhythmdb
import gobject
import os
import gtk

import load
import widgets.genreview
import widgets.entryview
import debug

menu_ui = """
<ui>
  <toolbar name="ToolBar">
    <separator/>
    <toolitem name="ShoutcastStaredStations" action="ShoutcastStaredStations"/>
  </toolbar>
</ui>
"""

class ShoutcastSource(rb.StreamingSource):

  __gproperties__ = {
    'plugin': (rb.Plugin,
      'plugin',
      'plugin',
      gobject.PARAM_WRITABLE | gobject.PARAM_CONSTRUCT_ONLY),
    'cache-dir': (gobject.TYPE_STRING,
      'cache directory',
      'plugin cache directory',
      '',
      gobject.PARAM_WRITABLE | gobject.PARAM_CONSTRUCT_ONLY),
  }
  
  db = None
  shell = None
  entry_type = None
  cache_dir = None
  plugin = None
    
  loadmanager = load.LoadManager()
  
  activated = False
  
  def __init__ (self):
    rb.Source.__init__(self, name=_("Shoutcast"))

  def do_set_property(self, property, value):
    if property.name == 'plugin':
      self.plugin = value
    elif property.name == 'cache-dir':
      self.cache_dir = value
    else:
      raise AttributeError, 'unknown property %s' % property.name

  def create(self):
      self.shell = self.get_property('shell')
      self.db = self.shell.props.db
      self.entry_type = self.get_property('entry-type')

      self.vbox_main = gtk.VPaned()
      self.genres_list = widgets.GenresView(self.db, rhythmdb.PROP_GENRE, _("Genres"))
      self.genres_list.connect('property-selected', self.genres_property_selected)
      self.genres_list.connect('property-selection-reset', self.genres_property_selection_reset)      
      self.stations_list = widgets.EntryView(self.db, self.shell.get_player(), self.plugin)
      vbox_1 = gtk.VBox()
      vbox_1.pack_start(self.genres_list)
      self.vbox_main.add1(vbox_1)
      self.vbox_main.add2(self.stations_list)
      self.vbox_main.show_all()
      self.add(self.vbox_main)
      
      manager = self.shell.get_player().get_property('ui-manager')
      action = gtk.Action('ShoutcastStaredStations', _('Show/Hide'),
          _("ShoutcastStaredStations"),
          'gtk-save')
      action.connect('activate', self.showhide)
      self.action_group = gtk.ActionGroup('ShoutcastPluginActions')
      self.action_group.add_action(action)
      manager.insert_action_group(self.action_group, 0)
      self.ui_id = manager.add_ui_from_string(menu_ui)
      manager.ensure_update()

      self.filter_genres_default_query()

      self.loadmanager.load(load.XmlGenresLoader(self.db, self.cache_dir, self.entry_type))

  def do_impl_get_entry_view(self):
    return self.stations_list

  def showhide(self):
    pass

  def filter_genres_default_query(self):
      genres_query = self.db.query_new()
      self.db.query_append(genres_query, (rhythmdb.QUERY_PROP_EQUALS, rhythmdb.PROP_TYPE, self.entry_type))
      genres_query_model = self.db.query_model_new_empty ()
      self.db.do_full_query_parsed(genres_query_model, genres_query)
      genres_props_model = self.genres_list.get_model()
      genres_props_model.set_property('query-model', genres_query_model)

  def filter_by_genre_clear(self):
      self.stations_query = self.db.query_new()
      self.stations_query_model = self.db.query_model_new_empty ()
      self.stations_list.set_model(self.stations_query_model)

  def filter_by_genre(self, genre):
      stations_query = self.db.query_new()
      self.db.query_append(stations_query, (rhythmdb.QUERY_PROP_EQUALS, rhythmdb.PROP_TYPE, self.entry_type))
      self.db.query_append(stations_query, (rhythmdb.QUERY_PROP_EQUALS, rhythmdb.PROP_GENRE, genre))
      self.db.query_append(stations_query, (rhythmdb.QUERY_PROP_LIKE, rhythmdb.PROP_KEYWORD, 'station'))
      self.stations_query_model = self.db.query_model_new_empty ()
      self.db.do_full_query_parsed(self.stations_query_model, stations_query)
      self.stations_list.set_model(self.stations_query_model)

      self.loadmanager.load(load.XmlStationsLoader(self.db, self.cache_dir, self.entry_type, genre))

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

    rb.Source.do_impl_activate(self)

gobject.type_register(ShoutcastSource)