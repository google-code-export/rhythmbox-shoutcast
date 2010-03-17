import rhythmdb
import gtk
import rbdb

class TreeSmartSearch:
  
  # GtkTreeView
  treeview = None
  # GtkTreeModelFilter
  treeviewmodel = None
  searchentry = None
  
  def __init__(self, db):
    self.db = db
  
  def catch_treecontrol(self, widget):
    if isinstance(widget, gtk.TreeView):
      self.treeview = widget
  
  def connect_to_tree(self, container, searchentry):
    self.container = container
    
    container.foreach(self.catch_treecontrol)
    
    if not self.treeview:
      raise Exception('Unable to find treeview')
    
    self.create()
    
    self.searchentry = searchentry
    self.searchentry.set_callback(self.new_filter_text)
    self.searchentry.set_focus_back(self.treeview)
    
  def create(self):
    self.treeview.set_property('enable-search', False)
    self.treeview.connect('key-press-event', self.keyboard_event)
    
  def keyboard_event(self, treeview, event):
    if self.searchentry.scope_event(event):
      self.searchentry.show_entry(event)
      return True
    
    if event.keyval == gtk.keysyms.Escape:
      self.searchentry.hide_entry()
      return True
  
  def set_model(self, model):
    self.searchentry.hide_entry()
    
    self.model = model
    self.treeviewmodel = self.db.query_model_new_empty()
    query = self.db.query_new()
    self.treeviewmodel.set_query(query)
    self.treeviewmodel.set_property('base-model', self.model)

  def filter_model(self, model):
    self.set_model(model)
    return self.treeviewmodel

  def new_filter_text(self, text):
    query = self.db.query_new()
    self.db.query_append(query, (rhythmdb.QUERY_PROP_LIKE, rhythmdb.PROP_TITLE, text))
    self.treeviewmodel.set_query(query)
    self.treeviewmodel.set_property('base-model', self.model)
    self.treeviewmodel.reapply_query(True)
    
    url = self.container.get_entry_url()
    if url:
      entry = self.db.entry_lookup_by_location(url)
      if entry:
        self.container.scroll_to_entry(entry)
