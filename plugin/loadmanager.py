from collections import deque
import gobject

class LoadManager:
  
  stack = deque()
  notify_id = 0
  
  def __init__(self):
    pass
  
  def load(self, xmlloader):
    xmlloader.set_callback(self.notify_status_changed)
    self.stack.append(xmlloader)
    
    self.notify_status_changed()
    
  def checkstatus(self):
    if self.stack.__len__() > 0:
      xmlloader = self.stack[0]
      
      if xmlloader.fresh():
        xmlloader.update()
        self.notify_status_changed()
      
      if xmlloader.done():
        self.stack.popleft()
        self.notify_status_changed()    
    
  def notify_status_changed(self):  
    if self.notify_id == 0:
      self.notify_id = gobject.idle_add(self.change_idle_cb)

  def change_idle_cb(self):
    self.notify_status_changed()
    self.notify_id = 0
      
    self.checkstatus()
    
    return False