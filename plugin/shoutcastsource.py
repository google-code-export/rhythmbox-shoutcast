import rb, rhythmdb
import gobject, os, gtk, gconf, gnome
import load, widgets, debug

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
  filter = False
  genre = None
  
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
      self.gconf = gconf.client_get_default()

      self.create_window()
      self.create_toolbar()

      self.load_config()

      self.filter_genres_default_query()

      self.sync_control_state()

  def create_window(self):
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

  def create_toolbar(self):
    icon_file_name = self.plugin.find_file("widgets/filter.png")
    iconsource = gtk.IconSource()
    iconsource.set_filename(icon_file_name)
    iconset = gtk.IconSet()
    iconset.add_source(iconsource)
    
    iconfactory = gtk.IconFactory()
    iconfactory.add("filter-icon", iconset)
    iconfactory.add_default()

    manager = self.shell.get_player().get_property('ui-manager')
    action = gtk.ToggleAction('ShoutcastStaredStations', _('Show/Hide'),
        _("Show/Hide stared stations in the list"),
        'filter-icon')
    action.connect('activate', self.showhide_stations)
    self.action_group = gtk.ActionGroup('ShoutcastPluginActions')
    self.action_group.add_action(action)
    manager.insert_action_group(self.action_group, 0)
    self.ui_id = manager.add_ui_from_string(menu_ui)
    manager.ensure_update()

  def load_config(self):
    self.filter = bool(self.gconf.get_int('/apps/rhythmbox/plugins/shoutcast/filter'))
    self.vbox_main.set_position(self.gconf.get_int('/apps/rhythmbox/plugins/shoutcast/genres_height'))

  def save_config(self):
    self.gconf.set_int('/apps/rhythmbox/plugins/shoutcast/filter', self.filter)
    self.gconf.set_int('/apps/rhythmbox/plugins/shoutcast/genres_height', self.vbox_main.get_position())

  def do_impl_get_entry_view(self):
    return self.stations_list

  def showhide_stations(self, control):
    action = self.action_group.get_action('ShoutcastStaredStations')
    self.filter = action.get_active()
    
    self.filter_genres_default_query()
    if self.genre:
      self.filter_by_genre()

  def sync_control_state(self):
    action = self.action_group.get_action('ShoutcastStaredStations')
    action.set_active(self.filter)

  def filter_genres_default_query(self):
    genres_query = self.db.query_new()
    self.db.query_append(genres_query, (rhythmdb.QUERY_PROP_EQUALS, rhythmdb.PROP_TYPE, self.entry_type))
    if self.filter:
      self.db.query_append(genres_query, (rhythmdb.QUERY_PROP_LIKE, rhythmdb.PROP_KEYWORD, 'star'))
    genres_query_model = self.db.query_model_new_empty ()
    self.db.do_full_query_parsed(genres_query_model, genres_query)
    genres_props_model = self.genres_list.get_model()
    genres_props_model.set_property('query-model', genres_query_model)

    # do not update genres when filter active (no need, favorite mode mean local stations)
    if not self.filter:
      self.loadmanager.load(load.XmlGenresLoader(self.db, self.cache_dir, self.entry_type))

  def filter_by_genre_clear(self):
    self.stations_query = self.db.query_new()
    self.stations_query_model = self.db.query_model_new_empty ()
    self.stations_list.set_model(self.stations_query_model)

  def filter_by_genre(self):
    stations_query = self.db.query_new()
    self.db.query_append(stations_query, (rhythmdb.QUERY_PROP_EQUALS, rhythmdb.PROP_TYPE, self.entry_type))
    self.db.query_append(stations_query, (rhythmdb.QUERY_PROP_EQUALS, rhythmdb.PROP_GENRE, self.genre))
    self.db.query_append(stations_query, (rhythmdb.QUERY_PROP_LIKE, rhythmdb.PROP_KEYWORD, 'station'))
    if self.filter:
      self.db.query_append(stations_query, (rhythmdb.QUERY_PROP_LIKE, rhythmdb.PROP_KEYWORD, 'star'))
    self.stations_query_model = self.db.query_model_new_empty ()
    self.db.do_full_query_parsed(self.stations_query_model, stations_query)
    self.stations_list.set_model(self.stations_query_model)

    # do not update station when filter active (no need, favorite mode mean local stations)
    if not self.filter:
      self.loadmanager.load(load.XmlStationsLoader(self.db, self.cache_dir, self.entry_type, self.genre))

  def genres_property_selected(self, view, name):
    ens = self.genres_list.get_selection()
    if not ens:
      self.filter_by_genre_clear()
    else:
      self.genre = ens[0]
      self.filter_by_genre()

  def genres_property_selection_reset(self):
    self.filter_by_genre_clear()

  def do_impl_activate(self):
    if not self.activated:
      self.activated = True
      self.create()

    rb.Source.do_impl_activate(self)

  def do_impl_deactivate(self):
    self.save_config()

gobject.type_register(ShoutcastSource)