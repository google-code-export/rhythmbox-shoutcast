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
    
    self.append(xmlloader)
    
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
    self.__notify_status_changed();

  def append(self, loader):
    # move exiting entry to the top
    for i in self.stack:
      if i.file_url == loader.file_url:
        self.stack.remove(i)
        self.stack.append(loader)
        return
    # or just add to the top
    self.stack.append(loader)

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
