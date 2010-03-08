import gobject

class LoadManager:
  
  stack = []
  xmlloader = None
  notify_id = 0
  
  def __init__(self):
    pass
  
  def load(self, xmlloader):
    xmlloader.set_callback(self.notify_status_changed)
    self.stack.append(xmlloader)
    
    self.notify_status_changed()
    
  def checkstatus(self):
    if self.xmlloader:
      if self.xmlloader.fresh():
        self.xmlloader.update()
        self.notify_status_changed()
      
      if self.xmlloader.done():
        self.xmlloader = None
        self.notify_status_changed()
            
    elif self.stack.__len__() > 0:
      self.xmlloader = self.stack.pop()
      self.notify_status_changed()    
    
  def notify_status_changed(self):  
    if self.notify_id == 0:
      self.notify_id = gobject.idle_add(self.change_idle_cb)

  def change_idle_cb(self):
    self.notify_status_changed()
    self.notify_id = 0
      
    self.checkstatus()
    
    return False