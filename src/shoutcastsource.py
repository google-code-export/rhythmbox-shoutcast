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
import gobject, os, gtk, gconf, gnome
import load, widgets, debug, service, rbdb, service
import xmlstore
import traceback, sys, urllib

menu_ui = """
<ui>

  <menubar name="MenuBar">
    <menu name="MusicMenu" action="Music">
      <placeholder name="PluginPlaceholder">
        <menu name="ShoutcastMenu" action="ShoutcastMenu">
          <menuitem name="ImportShoutcast" action="ImportShoutcast"/>
          <menuitem name="ExportShoutcast" action="ExportShoutcast"/>
        </menu>
      </placeholder>
    </menu>
  </menubar>

  <popup name="ShoutcastSourceMainPopup">
    <menuitem name="ImportShoutcast" action="ImportShoutcast"/>
    <menuitem name="ExportShoutcast" action="ExportShoutcast"/>
  </popup>

  <popup name="ShoutcastGenresViewPopup">
    <menuitem name="ReloadGenres" action="ReloadGenres"/>
    <menuitem name="ReloadStations" action="ReloadStations"/>
  </popup>

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
    'data-dir': (gobject.TYPE_STRING,
      'data directory',
      'plugin data directory',
      '',
      gobject.PARAM_WRITABLE | gobject.PARAM_CONSTRUCT_ONLY),
  }
  
  # rhythmbox rhythmdb object
  db = None

  # rhythmbox shell object
  shell = None

  # rhythmbox rhythmdb entry_type object
  entry_type = None
  cache_dir = None
  data_dir = None
  plugin = None
  loadmanager = None
  
  # form was activated (user clicked on rhythmbox left pane with this plugin name)
  activated = False
  
  # main window was created, and we need save window settings on exit
  main_window = False
  
  filter = False
  vbox_main = None
  genres_list = None
  stations_list = None
  
  # if checked we cache SHOUTcast playlists localy in rhythmbox database
  cache_stations_locally = False
  
  # database fully loaded. after rhythmbox starts to load database in parallel thread. we need
  # to wait until it fully loaded. 
  load_complete = False
  
  info_available_id = 0
  
  # apikey. SHOUTcast API 2.0 developer key.
  apikey = None
  apicheck = None
  
  def __init__ (self):
    rb.StreamingSource.__init__(self, name=_("SHOUTcast"))

  def do_set_property(self, property, value):
    if property.name == 'plugin':
      self.plugin = value
    elif property.name == 'cache-dir':
      self.cache_dir = value
    elif property.name == 'data-dir':
      self.data_dir = value
    else:
      raise AttributeError, 'unknown property %s' % property.name

  def init(self):
    self.shell = self.get_property('shell')
    self.db = self.shell.props.db
    self.entry_type = self.get_property('entry-type')
    self.gconf = gconf.client_get_default()

    self.create_toolbar()
    
    self.db.connect('load-complete', self.db_load_complete)
    
    self.apicheck = service.ApikeyCheck(self.cache_dir)    
    self.apicheck.load_failed = self.api_load_failed
    self.apicheck.load_succesed = self.api_load_success
    self.apicheck.check()

  def create(self):
    self.loadmanager = load.LoadManager()
    self.loadmanager.load_callback(self.load_status_changed)

    self.db_default_query()    

    self.genres_list = widgets.GenresView(self.db, self.entry_type)
    self.stations_list = widgets.EntryView(self.db, self.shell.get_player(), self.plugin)

  def db_default_query(self):
    genres_query = self.db.query_new()
    self.db.query_append(genres_query, (rhythmdb.QUERY_PROP_EQUALS, rhythmdb.PROP_TYPE, self.entry_type))
    genres_query_model = self.db.query_model_new_empty ()
    self.db.do_full_query_parsed(genres_query_model, genres_query)
    self.set_property('query-model', genres_query_model)
    
  def db_load_complete(self, db):
    self.load_complete = True

    # create form only if it was activated already
    if self.activated:
      self.create_form()
    
  def create_form(self):

    # do not recreate main window if its alreay created, app can die due (raise exception) to mess with events
    if self.main_window:
      return
    
    if self.apikey is None or len(self.apikey) == 0:
      self.create_aol_form()
    elif self.activated and self.load_complete:
      self.create_mainwindow()
    else:
      self.create_splashscreen()

  def create_mainwindow(self):
    self.main_window = True
    
    service.check_and_serve(self.db, self.entry_type)

    self.create_window()

    self.load_config()

    self.sync_control_state()
    
    self.connect_all()

  def create_splashscreen(self):
    if self.vbox_main:
      self.remove(self.vbox_main)
      self.vbox_main.hide_all()
      self.vbox_main = None

    self.vbox_main = gtk.VBox()
    
    label_1 = gtk.Label('Loading...')
    self.vbox_main.pack_start(label_1)
    label_2 = gtk.Label('(If you just added SHOUTcast plugin, please restart the rhythmbox player due to bug in rhythmdb)')
    self.vbox_main.pack_start(label_2)
    
    self.vbox_main.show_all()
    self.add(self.vbox_main)

  def create_aol_form(self):
    if self.vbox_main:
      self.remove(self.vbox_main)
      self.vbox_main.hide_all()
      self.vbox_main = None

    self.vbox_main = gtk.VBox()
    
    label_1 = gtk.Label( 'Welcome to AOL (SHOUTcast API 2.0) singn up wizzard :) ...' )
    self.vbox_main.pack_start(label_1)
    if self.apicheck.check_result():
      label_2 = gtk.Label(str(self.apicheck.check_result()))
      label_2.set_line_wrap(True)
      self.vbox_main.pack_start(label_2)
      button = gtk.Button('Reload APIKEY')
      button.connect('clicked', self.api_reload, button)
      self.vbox_main.pack_start(button)
    else:
      label_2 = gtk.Label()
      label_2.set_line_wrap(True)
      label_2.set_markup( 'Getting SHOUTcast API 2.0 magic key from the network ...')
      self.vbox_main.pack_start(label_2)
    
    self.vbox_main.show_all()
    self.add(self.vbox_main)

  def connect_all(self):
    self.genres_list.connect('property-selected', self.genres_property_selected)
    self.genres_list.connect('property-selection-reset', self.genres_property_selection_reset)      
    action = self.action_group.get_action('ShoutcastStaredStations')
    action.connect('activate', self.do_showhide_stations)
    action = self.action_group.get_action('CopyURL')
    action.connect('activate', self.do_copy_url)
    action = self.action_group.get_action('ReloadGenres')
    action.connect('activate', self.do_reload_genres)
    action = self.action_group.get_action('ReloadStations')
    action.connect('activate', self.do_reload_stations)
    
    self.genres_list.connect('show_popup', self.do_genres_show_popup)
    self.stations_list.connect('show_popup', self.do_stations_show_popup)
    self.stations_list.connect('star', self.do_star_change)
    
    player = self.shell.get_property('shell-player')
    player.connect('playing-source-changed', self.playing_source_changed_cb)
    
  def create_window(self):
    if self.vbox_main:
      self.remove(self.vbox_main)
      self.vbox_main.hide_all()
      self.vbox_main = None

    self.vbox_main = gtk.VPaned()
    vbox_1 = gtk.VBox()
    vbox_1.pack_start(self.genres_list)
    self.vbox_main.pack1(vbox_1, True, False)
    vbox_2 = gtk.VBox()
    vbox_2.pack_start(self.stations_list)
    searchentry = widgets.SearchEntry()
    vbox_2.pack_start(searchentry, False)
    self.vbox_main.pack2(vbox_2, True, False)
    self.vbox_main.show_all()
    
    self.stations_list.set_searchentry(searchentry)
    
    self.add(self.vbox_main)

  def create_toolbar(self):
    filtersource = gtk.IconSource()
    filtersource.set_filename(self.plugin.find_file("widgets/filter.png"))
    filtericon = gtk.IconSet()
    filtericon.add_source(filtersource)    
    shoutcastsource = gtk.IconSource()
    shoutcastsource.set_filename(self.plugin.find_file("shoutcast.png"))
    shoutcasticon = gtk.IconSet()
    shoutcasticon.add_source(shoutcastsource)    
    iconfactory = gtk.IconFactory()
    iconfactory.add('filter-icon', filtericon)
    iconfactory.add('shoutcast-icon', shoutcasticon)
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
    action = gtk.Action('ReloadGenres', _('Reload genres list'),
        _("Reload genres list from the shoutcast server"),
        'gtk-refresh')
    self.action_group.add_action(action)
    action = gtk.Action('ReloadStations', _('Reload stations'),
        _("Reload stations list for selected genre from the shoutcast server"),
        'gtk-refresh')
    self.action_group.add_action(action)
    action = gtk.Action('ImportShoutcast', _('Import Favorite stations ...'),
        _("Import Shoutcast favorite stations from OPML file"),
        'gtk-copy')
    self.action_group.add_action(action)
    action = gtk.Action('ExportShoutcast', _('Export Favorite stations ...'),
        _("Export Shoutcast favorite stations from OPML file"),
        'gtk-copy')
    self.action_group.add_action(action)
    action = gtk.Action('ShoutcastMenu', _('SHOUTcast'),
        _("ShoutcastMenu"),
        'shoutcast-icon')
    self.action_group.add_action(action)
    manager.insert_action_group(self.action_group, 0)
    self.ui_id = manager.add_ui_from_string(menu_ui)
    manager.ensure_update()

    action = self.action_group.get_action('ImportShoutcast')
    action.connect('activate', self.do_import_shoutcast)
    action = self.action_group.get_action('ExportShoutcast')
    action.connect('activate', self.do_export_shoutcast)

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
      
    self.gconf.suggest_sync()

  def do_impl_get_entry_view(self):
    return self.stations_list

  def do_showhide_stations(self, control):
    filter = self.filter
    
    action = self.action_group.get_action('ShoutcastStaredStations')
    self.filter = action.get_active()

    if self.genres_list.genre():
      self.genres_list.save_config()
      
    if self.stations_list.get_entry_url():
      self.stations_list.save_config()

    self.gconf.suggest_sync()

    self.load_positions()

  def load_positions(self):
    self.filter_genres_default_query()
    self.genres_list.load_config()

    if self.genres_list.genre():
      self.filter_by_genre(self.genres_list.genre())
      self.stations_list.load_config()
      
    if self.filter:
      self.stations_list.load_columns_filer()
    else:
      self.stations_list.load_columns()


  def do_copy_url(self, action):
    clipboard = gtk.clipboard_get()
    clipboard.set_text(self.stations_list.get_entry_url())

  def sync_control_state(self):
    action = self.action_group.get_action('ShoutcastStaredStations')
    action.set_active(self.filter)

  def filter_genres_default_query(self):
    self.genres_list.do_query(self.filter)

    # do not update genres until filter is active (cause it is no need, favorite mode works with local stations)
    if not self.filter:
      self.loadmanager.load(load.XmlGenresLoader(self.db, self.cache_dir, self.entry_type, self.apikey))

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

    # do not update genres until filter mode is active (cause that is no need, favorite mode works with local stations)
    if not self.filter:
      loader = load.XmlStationsLoader(self.db, self.cache_dir, self.data_dir, self.entry_type, genre, self.apikey)

      query = self.db.query_new()
      self.db.query_append(query, (rhythmdb.QUERY_PROP_EQUALS, rhythmdb.PROP_TYPE, self.entry_type))
      self.db.query_append(query, (rhythmdb.QUERY_PROP_EQUALS, rhythmdb.PROP_GENRE, genre))
      self.db.query_append(query, (rhythmdb.QUERY_PROP_LIKE, rhythmdb.PROP_KEYWORD, 'station'))
      query_model = self.db.query_model_new_empty()
      self.db.do_full_query_parsed(query_model, query)
      stations_here = query_model.get_iter_first()
  
      # do start download if is no stations here or it ready to update
      if not stations_here or loader.ready_to_update():
        self.loadmanager.load(loader)

  def genres_property_selected(self, view, name):
    genre = self.genres_list.genre()
    if genre:
      self.filter_by_genre(genre)
    else:
      self.filter_by_genre_clear()

  def genres_property_selection_reset(self):
    self.filter_by_genre_clear()

  def do_reload_stations(self, some):
    genre = self.genres_list.genre()
    if genre:
      loader = load.XmlStationsLoader(self.db, self.cache_dir, self.data_dir, self.entry_type, genre, self.apikey)
      loader.check_remove_target()
      self.loadmanager.load(loader)
  
  def do_reload_genres(self, some):
    loader = load.XmlGenresLoader(self.db, self.cache_dir, self.entry_type, self.apikey)
    loader.check_remove_target()
    self.loadmanager.load(loader)

  def do_genres_show_popup(self, entry):
    # rhythmbox api break up (0.13.2 - 0.13.3)
    if hasattr(rb, 'show_source_popup'):
      self.show_source_popup("/ShoutcastGenresViewPopup")
    else:
      self.show_page_popup("/ShoutcastGenresViewPopup")
  
    return True

  def do_stations_show_popup(self, entry, source):
    # rhythmbox api break up (0.13.2 - 0.13.3)
    if hasattr(rb, 'show_source_popup'):
      self.show_source_popup("/ShoutcastSourceViewPopup")
    else:
      self.show_page_popup("/ShoutcastSourceViewPopup")
    
    return True

  def do_impl_show_popup(self):
    # rhythmbox api break up (0.13.2 - 0.13.3)
    if hasattr(rb, 'show_source_popup'):
      self.show_source_popup("/ShoutcastSourceMainPopup")
    else:
      self.show_page_popup("/ShoutcastSourceMainPopup")

    return True

  # rhyhtmbox api break up (0.13.2 - 0.13.3)
  def do_impl_get_status(self):
    return self.do_get_status()
  
  def do_get_status(self):
    if self.loadmanager.load_progress():
      (text, progress) = self.loadmanager.load_get_progress()
      return (_("Loading Shoutcast stations"), text, progress)
    else:
      qm = self.get_property("query-model")
      return (qm.compute_status_normal("%d song", "%d songs"), None, 1)

  # rhyhtmbox api break up (0.13.2 - 0.13.3)
  def do_impl_activate(self):
    self.do_selected()

    rb.Source.do_impl_activate(self)
    
  def do_selected(self):
    if not self.activated:
      self.activated = True
      
      self.create()
      
      self.create_form()

  def do_impl_deactivate(self):
    if self.main_window:
      self.save_config()

  # rhythmbox api break up (0.13.2 - 0.13.3)
  def do_impl_get_ui_actions(self):
    return self.do_get_ui_actions()
  
  def do_get_ui_actions(self):
    return ["ShoutcastStaredStations"]

  def load_status_changed(self):
    self.emit('status-changed')

  def do_import_shoutcast(self, obj):
    file_open = gtk.FileChooserDialog(title="Select OPML file"
          , action=gtk.FILE_CHOOSER_ACTION_OPEN
          , buttons=(gtk.STOCK_CANCEL
                , gtk.RESPONSE_CANCEL
                , gtk.STOCK_OPEN
                , gtk.RESPONSE_OK))

    filter = gtk.FileFilter()
    filter.set_name("OPML")
    filter.add_pattern("*.opml")
    file_open.add_filter(filter)

    filter = gtk.FileFilter()
    filter.set_name(_("All files"))
    filter.add_pattern("*")
    file_open.add_filter(filter)
    
    if file_open.run() == gtk.RESPONSE_OK:
      result = file_open.get_filename()
      
      try:
        opml = xmlstore.ShoutcastOPML()
        opml.read(result)
        opml.save(self.db, self.data_dir, self.entry_type)
      except Exception as e:
        file_open.destroy()
        self.show_error(service.ft())

    file_open.destroy()

  def do_export_shoutcast(self, obj):
    file_save = gtk.FileChooserDialog(title="Save OPML file"
          , action=gtk.FILE_CHOOSER_ACTION_SAVE
          , buttons=(gtk.STOCK_CANCEL
                , gtk.RESPONSE_CANCEL
                , gtk.STOCK_SAVE
                , gtk.RESPONSE_OK))

    filter = gtk.FileFilter()
    filter.set_name("OPML")
    filter.add_pattern("*.opml")
    file_save.add_filter(filter)

    filter = gtk.FileFilter()
    filter.set_name(_("All files"))
    filter.add_pattern("*")
    file_save.add_filter(filter)
    
    file_save.set_current_name('shoutcast-favorites.opml')
    
    if file_save.run() == gtk.RESPONSE_OK:
      result = file_save.get_filename()
      
      try:
        opml = xmlstore.ShoutcastOPML()
        opml.load(self.db, self.entry_type)
        opml.write(result)
      except Exception as e:
        file_save.destroy()
        self.show_error(service.ft())

    file_save.destroy()

  def do_star_change(self, entryview, model, iter):
    entry = rbdb.iter_to_entry(self.db, model, iter)
    star = self.db.entry_keyword_has(entry, 'star')
    title = self.db.entry_get(entry, rhythmdb.PROP_TITLE)
    
    if star and self.cache_stations_locally:
      url = self.db.entry_get(entry, rhythmdb.PROP_LOCATION)
      if load.playlist_isfilename(url):
        playlist = load.PlaylistLoader(self.data_dir, load.playlist_filename2url(url), title)
      else:
        playlist = load.PlaylistLoader(self.data_dir, url, title)
        playlist.playlist_callback(self.do_star_update_url)

      self.loadmanager.load(playlist)

  def do_star_update_url(self, loader):
    entry = self.db.entry_lookup_by_location(loader.url)
    title = self.db.entry_get(entry, rhythmdb.PROP_TITLE)
    self.db.set(entry, rhythmdb.PROP_LOCATION, load.playlist_filename_url(self.data_dir, loader.url, title))
    self.db.commit()

  def show_error(self, message):
    parent = self.shell.get_property('window')
    dialog = gtk.MessageDialog(parent, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, message)    
    
    dialog.run()
    dialog.destroy()

  def playing_source_changed_cb(self, player, source):
    backend = player.get_property('player')
    
    if not self.info_available_id:
      self.info_available_id = backend.connect('info', self.info_available_cb)
    else:
      backend.disconnect(self.info_available_id)
      self.info_available_id = 0

  def info_available_cb(self, backend, uri, field, value):
    player = self.shell.get_player()
    entry = player.get_playing_entry()
    if field == 0: # RB_METADATA_FIELD_TITLE:
      self.set_streaming_title(value)
    elif field == 1: # RB_METADATA_FIELD_ARTIST
      self.streaming_artist(value)
    elif field == 4: # RB_METADATA_FIELD_GENRE
      pass # RHYTHMDB_PROP_GENRE
    elif field == 19: # RB_METADATA_FIELD_CODEC
      pass # self.db.set(entry, rhythmdb.PROP_MIMETYPE, value)
    elif field == 20: # RB_METADATA_FIELD_BITRATE
      pass # self.db.set(entry, rhythmdb.PROP_BITRATE, value)
      
  def api_reload(self, event, button):
    button.set_state(gtk.STATE_INSENSITIVE)
    self.apicheck.check()
  
  def api_load_failed(self):
    if self.apicheck.apikey_file_exist():
      debug.log('Load APIKEY failed with: ' + str(self.apicheck.check_result()))
      self.apicheck.apikey_load()
      return
      
    if self.activated:
      self.create_form()
  
  def api_load_success(self):
    self.apikey = self.apicheck.apikey
    
    # create form only if it already been activated. othervise we done download apikey file earlier before any
    # action was taked by rhythmbox.
    
    if self.activated:
      self.create_form()

gobject.type_register(ShoutcastSource)