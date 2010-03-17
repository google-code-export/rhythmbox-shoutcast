import gtk

class TreeSmartSearchWindow(gtk.Window):
  
  __callback = None
  treeview = None
  
  def __init__(self, treeview):
    gtk.Window.__init__(self, gtk.WINDOW_POPUP)

    self.treeview = treeview

    toplevel = treeview.get_toplevel()
    screen = treeview.get_screen()
    self.set_screen(screen)
    
    #if toplevel.get_group():
    #  toplevel.get_group().add_window(self)

    self.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_UTILITY)
    self.connect('delete-event', self.search_delete_event)
    self.connect('key-press-event', self.search_key_press_event)
    self.connect('scroll-event', self.search_scroll_event)
    
    self.search_entry = gtk.Entry()
    self.search_entry.connect('activate', self.search_activate)
    self.search_entry.connect('changed', self.changed)
    self.search_entry.set_property('primary-icon-stock', 'gtk-find')
    self.search_entry.set_property('secondary-icon-stock', 'gtk-clear')
    self.search_entry.connect('icon-release', self.icon_release)

    vbox = gtk.VBox(False, 0)
    vbox.set_border_width(3)
    vbox.add(self.search_entry)

    frame = gtk.Frame()
    frame.set_shadow_type(gtk.SHADOW_ETCHED_IN)
    frame.add(vbox)
    
    frame.show_all()
    
    self.add(frame)
  
    self.search_entry.realize()

  def position_func(self, treeview):
    tree_window = treeview.get_bin_window()
    screen = treeview.get_screen()
    monitor_num = screen.get_monitor_at_window(tree_window)
    monitor = screen.get_monitor_geometry(monitor_num)
    
    self.realize()
    
    (tree_x, tree_y) = tree_window.get_origin()
    (tree_width, tree_height) = tree_window.get_size()
    (requisition_width, requisition_height) = self.size_request()

    if tree_x + tree_width > screen.get_width():
      x = screen.get_width() - requisition_width;
    elif tree_x + tree_width - requisition_width < 0:
      x = 0
    else:
      x = tree_x + tree_width - requisition_width
  
    if tree_y + tree_height + requisition_height > screen.get_height():
      y = screen.get_height() - requisition_height
    elif tree_y + tree_height < 0:
      y = 0
    else:
      y = tree_y + tree_height;
  
    self.move(x, y);

  def search_delete_event(self, event):
    self.hide_dialog()
  
  def search_key_press_event(self, window, event):
    if (event.keyval == gtk.keysyms.Escape or
      event.keyval == gtk.keysyms.Tab or
      event.keyval == gtk.keysyms.KP_Tab or
      event.keyval == gtk.keysyms.ISO_Left_Tab):
      self.hide_dialog()
      return True
      
    if (event.keyval == gtk.keysyms.Up or
      event.keyval == gtk.keysyms.KP_Up):
      self.__up_callback()
      return True

    if (event.keyval == gtk.keysyms.Down or
      event.keyval == gtk.keysyms.KP_Down):
      self.__down_callback()
      return True
  
  def icon_release(self, window, icon_pos, event):
    if icon_pos == gtk.ENTRY_ICON_SECONDARY:
      self.hide_dialog()
  
  def search_scroll_event(self, window, event):
    if event.direction == gtk.gdk.SCROLL_UP:
      self.__up_callback()
    
    if event.direction == gtk.gdk.SCROLL_DOWN:
      self.__down_callback()

  def set_callbacks(self, text_callback, up_callback, down_callback):
    self.__text_callback = text_callback
    self.__up_callback = up_callback
    self.__down_callback = down_callback
    
  def changed(self, s1):
    text = self.search_entry.get_text()
    self.__text_callback(text)
  
  def search_activate(self, window):
    self.hide_dialog()

  def hide_dialog(self):
    self.hide()
    self.search_entry.set_text('')

  def show_dialog(self):
    self.position_func(self.treeview)
    self.show()
    self.grab_focus()
