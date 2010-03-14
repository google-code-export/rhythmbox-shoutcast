import rb, rhythmdb
import gobject, os, gtk, gconf, gnome
import load, widgets, debug

menu_ui = """
<ui>
  <popup name="ShoutcastSourceViewPopup">
    <menuitem name="CopyURL" action="CopyURL"/>
  </popup>
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
  
  def __init__ (self):
    rb.Source.__init__(self, name=_("Shoutcast"))
    
    self.loadmanager.load_callback(self.load_status_changed)

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

    self.sync_control_state()
    
    self.connect_all()

  def connect_all(self):
    self.genres_list.connect('property-selected', self.genres_property_selected)
    self.genres_list.connect('property-selection-reset', self.genres_property_selection_reset)      
    action = self.action_group.get_action('ShoutcastStaredStations')
    action.connect('activate', self.showhide_stations)
    action = self.action_group.get_action('CopyURL')
    action.connect('activate', self.copy_url)
    
    self.stations_list.connect('show_popup', self.do_impl_show_popup)
    
  def create_window(self):
    self.vbox_main = gtk.VPaned()
    self.genres_list = widgets.GenresView(self.db, rhythmdb.PROP_GENRE, _("Genres"))
    self.stations_list = widgets.EntryView(self.db, self.shell.get_player(), self.plugin)
    vbox_1 = gtk.VBox()
    vbox_1.pack_start(self.genres_list)
    self.vbox_main.pack1(vbox_1, True, False)
    self.vbox_main.pack2(self.stations_list, True, False)
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
    self.action_group = gtk.ActionGroup('ShoutcastPluginActions')
    action = gtk.ToggleAction('ShoutcastStaredStations', _('Favorites'),
        _("Filter lists by favorite stations only"),
        'filter-icon')
    self.action_group.add_action(action)
    action = gtk.Action('CopyURL', _('Copy station URL'),
        _("Copy station URL to clipboard"),
        'gtk-copy')
    self.action_group.add_action(action)
    manager.insert_action_group(self.action_group, 0)
    self.ui_id = manager.add_ui_from_string(menu_ui)
    manager.ensure_update()

  def load_config(self):
    self.filter = bool(self.gconf.get_int('/apps/rhythmbox/plugins/shoutcast/filter'))
    self.vbox_main.set_position(self.gconf.get_int('/apps/rhythmbox/plugins/shoutcast/genres_height'))
    
    self.load_positions()

  def save_config(self):
    self.gconf.set_int('/apps/rhythmbox/plugins/shoutcast/filter', self.filter)
    self.gconf.set_int('/apps/rhythmbox/plugins/shoutcast/genres_height', self.vbox_main.get_position())
    
    if self.genres_list.genre():
      self.genres_list.save_config()
    if self.stations_list.get_entry_url():
      self.stations_list.save_config()

  def do_impl_get_entry_view(self):
    return self.stations_list

  def showhide_stations(self, control):
    filter = self.filter
    
    action = self.action_group.get_action('ShoutcastStaredStations')
    self.filter = action.get_active()

    if self.genres_list.genre():
      self.genres_list.save_config()
      
    if self.stations_list.get_entry_url():
      self.stations_list.save_config()

    self.load_positions()

  def load_positions(self):
    self.filter_genres_default_query()
    self.genres_list.load_config()

    if self.genres_list.genre():
      self.filter_by_genre(self.genres_list.genre())
      self.stations_list.load_config()

  def copy_url(self, action):
    clipboard = gtk.clipboard_get()
    clipboard.set_text(self.stations_list.get_entry_url())

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

  def filter_by_genre(self, genre):
    stations_query = self.db.query_new()
    self.db.query_append(stations_query, (rhythmdb.QUERY_PROP_EQUALS, rhythmdb.PROP_TYPE, self.entry_type))
    self.db.query_append(stations_query, (rhythmdb.QUERY_PROP_EQUALS, rhythmdb.PROP_GENRE, genre))
    self.db.query_append(stations_query, (rhythmdb.QUERY_PROP_LIKE, rhythmdb.PROP_KEYWORD, 'station'))
    if self.filter:
      self.db.query_append(stations_query, (rhythmdb.QUERY_PROP_LIKE, rhythmdb.PROP_KEYWORD, 'star'))
    self.stations_query_model = self.db.query_model_new_empty ()
    self.db.do_full_query_parsed(self.stations_query_model, stations_query)
    self.stations_list.set_model(self.stations_query_model)

    # do not update station when filter active (no need, favorite mode mean local stations)
    if not self.filter:
      self.loadmanager.load(load.XmlStationsLoader(self.db, self.cache_dir, self.entry_type, genre))

  def genres_property_selected(self, view, name):
    genre = self.genres_list.genre()
    if genre:
      self.filter_by_genre(genre)
    else:
      self.filter_by_genre_clear()

  def genres_property_selection_reset(self):
    self.filter_by_genre_clear()

  def do_impl_show_popup(self, entry, source):
    self.show_source_popup("/ShoutcastSourceViewPopup")
    
    return True

  def do_impl_get_status(self):
    if self.loadmanager.load_progress():
      (text, progress) = self.loadmanager.load_get_progress()
      return (_("Loading Shoutcast stations"), text, progress)
    else:
      qm = self.genres_list.get_model().get_property("query-model")
      return (qm.compute_status_normal("%d song", "%d songs"), None, 1)

  def do_impl_activate(self):
    if not self.activated:
      self.activated = True
      self.create()

    rb.Source.do_impl_activate(self)

  def do_impl_deactivate(self):
    self.save_config()

  def do_impl_get_ui_actions(self):
    return ["ShoutcastStaredStations"]

  def load_status_changed(self):
    self.emit('status-changed')

gobject.type_register(ShoutcastSource)