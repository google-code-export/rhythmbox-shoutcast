import gobject

import debug

class LoadManager:
  
  stack = []
  xmlloader = None
  notify_id = 0
  
  def __init__(self):
    pass
  
  def load(self, xmlloader):
    xmlloader.loader_callback(self.loader_changed)
    self.stack.append(xmlloader)
    
    self.checkstatus()

  def loader_changed(self):
    self.checkstatus()

  def checkstatus(self):
    if self.xmlloader:
      if self.xmlloader.loader_fresh():
        self.xmlloader.loader_update()
        return

      if not self.xmlloader.loader_progress():
        if self.xmlloader.loader_result():
          debug.log(self.xmlloader.loader_result())
        self.xmlloader = None
        self.checkstatus()
        return

    elif self.stack.__len__() > 0:
      self.xmlloader = self.stack.pop()
      self.checkstatus()
      return
