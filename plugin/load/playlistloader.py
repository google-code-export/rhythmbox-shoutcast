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

import rhythmdb
import xml.sax, xml.sax.handler, shutil, os, os.path, urlparse, urllib
import rbdb, debug

from xmlloader import *
from xmlstationshandler import *

def playlist_filename(data_dir, url, title):
  # create filename from the url of shoutcast station
  
  urlp = urlparse.urlparse(url)
  query = urlparse.parse_qs(urlp.query)
  
  id = int(query['id'][0])
  genre = urllib.quote(query['genre'][0])

  return os.path.join(data_dir, "id=%d&genre=%s&star=%s" % (id, genre, title))

def playlist_filename_url(data_dir, url, title):
  path = playlist_filename(data_dir, url, title)
  return "file://" + urllib.pathname2url(path)

def playlist_filename2url(file_url):
  name = path.basename(file_url)
  
  query = urlparse.parse_qs(name)
  
  id = int(query['id'][0])
  genre = urllib.quote(query['genre'][0])
  title = urllib.quote(query['star'][0])

  return xmlstation_encodeurl(id, genre)

def playlist_isfilename(file_url):
  return file_url.startswith('file')

class PlaylistLoader(CheckDownload):

  fresh = True

  error = None
  title = None

  __playlistcallback = None
  
  __callback = None
  __notify_id = 0

  def __init__(self, data_dir, url, title):
    CheckDownload.__init__(self, playlist_filename(data_dir, url, title),
                       url)

    self.title = title

    self.url = url

    self.check_callback(self.download_state)

  def loader_progress(self):
    # return true if loader is busy, still downloading / parsing
    if self.error:
      return False
    
    if self.check_progress():
      return True
   
    return False

  def loader_callback(self, callback):
    self.__callback = callback
    
  def playlist_callback(self, callback):
    self.__playlistcallback = callback

  def loader_fresh(self):
    # just added download, fresh, not yet started
    return self.fresh

  def loader_update(self):
    # do start your job, start to download / parse
    self.fresh = False
    self.update_catalogue()

  def loader_result(self):
    # after loader_progress, call for result (text or error)
    return self.error

  def loader_get_progress(self):
    # return progress in tuple (text, progress 0.0 - 1.0)
    if self.check_progress():
      return ("Downloading %s" % (self.title), self.check_get_progress()[1])
    else:
      return ("Downloaded playlist", -1)

  def set_error(self, e):
    # any error put here, we'll return it with loader_result
    self.error = e

  def download_state(self):
    # after check (super class, downloading progress) is done, it call this function.
    if self.check_progress():
      return
    
    if self.check_result():
      self.set_error(self.check_result())
      self.__notify_status_changed()
      return
    
    if self.__playlistcallback:
      self.__playlistcallback(self)
      
    self.__notify_status_changed()

  def update_catalogue(self):
    # do download
    self.check_update()
    self.__notify_status_changed()

  def __notify_status_changed(self):  
    if self.__notify_id == 0:
      self.__notify_id = gobject.idle_add(self.__change_idle_cb)

  def __change_idle_cb(self):
    self.__notify_status_changed()
    self.__notify_id = 0
    
    if self.__callback:
      self.__callback()

    return False
