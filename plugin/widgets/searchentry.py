import gtk, string

class SearchEntry(gtk.Frame):

  def __init__(self):
    gtk.Frame.__init__(self)
        
    self.search_entry = gtk.Entry()
    self.search_entry.connect('key-release-event', self.key_release_event)
    self.search_entry.connect('key-press-event', self.key_press_event)
    self.search_entry.connect('changed', self.changed)
    self.search_entry.set_property('primary-icon-stock', 'gtk-find')
    self.search_entry.set_property('secondary-icon-stock', 'gtk-clear')
    self.search_entry.connect('icon-release', self.icon_release)
    self.search_entry.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(251,249,107))
    
    self.set_property('no-show-all', True)

    vbox = gtk.VBox(False, 0)
    vbox.set_border_width(3)
    vbox.add(self.search_entry)

    vbox.show_all()

    self.set_shadow_type(gtk.SHADOW_ETCHED_IN)
    self.add(vbox)

  def changed(self, widget):
    self.__text(self.search_entry.get_text())

  def set_focus_back(self, focus):
    self.__focus = focus

  def set_callback(self, text):
    self.__text = text

  def key_press_event(self, widget, event):
    if event.keyval in [gtk.keysyms.KP_Up, gtk.keysyms.Up, gtk.keysyms.KP_Down, gtk.keysyms.Down]:
      self.__focus.grab_focus()
      return True
    
    return False

  def key_release_event(self, widget, event):
    print event.keyval, gtk.gdk.keyval_name(event.keyval)
    if event.keyval in [gtk.keysyms.Escape, gtk.keysyms.Return, gtk.keysyms.KP_Enter]:
      self.hide_entry()
      return True
        
    return False

  def empty(self):
    return len(self.search_entry.get_text()) == 0

  def scope_event(self, event):
    if gtk.gdk.keyval_name(event.keyval) in string.ascii_letters:
      return True

    if gtk.gdk.keyval_name(event.keyval) in string.digits:
      return True

    if event.keyval in [gtk.keysyms.BackSpace]:
      return True

    if not self.empty():
      if event.keyval in [gtk.keysyms.space, gtk.keysyms.Return, gtk.keysyms.KP_Enter]:
        return True

    return False 

  def hide_entry(self):
    self.hide()
    self.search_entry.set_text('')
    
    self.__focus.grab_focus()

  def show_entry(self, event = None):
    self.show()
    self.grab_focus()
    position = self.search_entry.get_position()
    self.search_entry.grab_focus()
    self.search_entry.set_position(position)
    
    if event:
      self.search_entry.event(event)
  
  def icon_release(self):
    pass
  
  def process_event(self, event):
    self.search_entry.event(event)
    return True
  