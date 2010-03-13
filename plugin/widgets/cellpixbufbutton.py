import gtk, gobject

class CellPixbufButton(gtk.GenericCellRenderer):

  __gsignals__ = {
                  'toggled': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE,
                             (gtk.TreeModel, str, gtk.TreeIter)),
  }

  __gproperties__ = {
                     'pixbuf': (gtk.gdk.Pixbuf, 'pixbuf', 'pixbuf', gobject.PARAM_WRITABLE),
  }

  pixbuf = None

  def __init__(self):
    gtk.GenericCellRenderer.__init__(self)
    
    self.set_property('mode', gtk.CELL_RENDERER_MODE_ACTIVATABLE)

  def do_set_property(self, property, value):
    if property.name == 'pixbuf':
      self.pixbuf = value
    else:
      raise AttributeError, 'unknown property %s' % property.name

  def on_get_size(self, widget, cell_area):
    xoffset = 0
    yoffset = 0
    width = self.pixbuf.get_width()
    height = self.pixbuf.get_height()
    return (xoffset, yoffset, width, height)

  def on_render(self, window, widget, background_area, cell_area, expose_area, flags):
    (xoffset, yoffset, width, height) = self.get_size(widget, cell_area)
  
    xoffset += cell_area.x;
    yoffset += cell_area.y;
    width -= self.get_property('xpad') * 2;
    height -= self.get_property('ypad') * 2;
  
    draw_rect = cell_area.intersect((xoffset, yoffset, width, height)) 
    window.draw_pixbuf(None,
      self.pixbuf,
      draw_rect.x - xoffset,
      draw_rect.y - yoffset,
      draw_rect.x,
      draw_rect.y,
      draw_rect.width,
      draw_rect.height,
      gtk.gdk.RGB_DITHER_NORMAL,
      0, 0);

  def on_start_editing(self, event, widget, path, background_area, cell_area, flags):
    model = widget.get_model()
    iter = model.get_iter(path)
    
    self.emit('toggled', model, iter)

  def on_activate(self, event, widget, path, background_area, cell_area, flags):
    model = widget.get_model()
    iter = model.get_iter(path)
    
    self.emit('toggled', model, path, iter)

    return True

gobject.type_register(CellPixbufButton)
