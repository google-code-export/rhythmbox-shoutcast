import gobject

import debug

class LoadManager:
  
  stack = []
  xmlloader = None
  __notify_id = 0
  
  def __init__(self):
    pass
  
  def load(self, xmlloader):
    xmlloader.loader_callback(self.loader_changed)
    self.stack.append(xmlloader)
    
    self.checkstatus()
    self.__notify_status_changed();
    
  def load_callback(self, callback):
    self.__callback = callback
    
  def load_progress(self):
    return self.xmlloader != None
  
  def load_get_progress(self):
    (text, progress) = self.xmlloader.loader_get_progress()
    return ('[' + repr(len(self.stack)) + '] ' + text, progress)

  def loader_changed(self):
    self.checkstatus()

  def checkstatus(self):
    if self.xmlloader:
      if self.xmlloader.loader_fresh():
        self.xmlloader.loader_update()
        self.__notify_status_changed();
        return

      if not self.xmlloader.loader_progress():
        if self.xmlloader.loader_result():
          debug.log(self.xmlloader.loader_result())
        self.xmlloader = None
        self.checkstatus()
        self.__notify_status_changed();
        return

    elif self.stack.__len__() > 0:
      self.xmlloader = self.stack.pop()
      self.checkstatus()
      self.__notify_status_changed();
      return

  def __notify_status_changed(self):  
    if self.__notify_id == 0:
      self.__notify_id = gobject.idle_add(self.__change_idle_cb)

  def __change_idle_cb(self):
    self.__notify_status_changed()
    self.__notify_id = 0
    
    if self.__callback:
      self.__callback()

    return False
