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
import xml.sax, xml.sax.handler, datetime, urllib, time, os
import debug, rbdb

'''
station format example:

<station name="TechnoBase.FM - 24h Techno, Dance, Trance, House and More - 128k MP3" mt="audio/mpeg" id="7429" br="128" genre="Techno  Electronic  Dance" ct="We aRe oNe" lc="6993"/>

where:
  name - station name
  mt - mime type
  id - station id
  br - bitrate
  genre - genre
  ct - currently playing track
  lc - listener count
'''

def xmlstation_encodeurl(id, genre):
  return 'http://yp.shoutcast.com/sbin/tunein-station.pls?id=%d&genre=%s' % (id, urllib.quote(genre))

class XmlStationsHandler(xml.sax.handler.ContentHandler):

  def __init__(self, db, entry_type, genre, data_dir):
    xml.sax.handler.ContentHandler.__init__(self)
    self.db = db
    self.entry_type = entry_type
    self.genre = genre
    self.data_dir = data_dir

  def startElement(self, name, attrs):
    self.attrs = attrs

  def station_copy(old_url, new_url):
    entry_old = entry_lookup_by_location(old_url)
    entry_new = self.db.entry_new(entry_type, new_url)
    
    db.set(entry_new, rhythmdb.PROP_TITLE, title)
    db.set(entry_new, rhythmdb.PROP_GENRE, genre)
    db.set(entry_new, rhythmdb.PROP_MIMETYPE, mimetype)
    db.set(entry_new, rhythmdb.PROP_BITRATE, bitrate)
    db.entry_keyword_add(entry_new, 'station')

  def endElement(self, name):
    if name == 'station':
      
      genre = self.genre
      id = int(self.attrs['id'])
      title = self.attrs['name']
      bitrate = int(self.attrs['br'])
      mimetype = self.attrs['mt']
      
      track_url = xmlstation_encodeurl(id, genre)

      from playlistloader import playlist_filename_url
      track_url_star = playlist_filename_url(self.data_dir, track_url, title)

      entry = rbdb.entry_lookup_by_location(self.db, track_url_star)
      if entry == None:
        entry = rbdb.entry_lookup_by_location(self.db, track_url)
        if entry == None:
          entry = self.db.entry_new(self.entry_type, track_url)
          debug.log("New station: " + title)

      self.db.set(entry, rhythmdb.PROP_TITLE, title)
      self.db.set(entry, rhythmdb.PROP_GENRE, genre)
      self.db.set(entry, rhythmdb.PROP_MIMETYPE, mimetype)
      self.db.set(entry, rhythmdb.PROP_BITRATE, bitrate)
      self.db.entry_keyword_remove(entry, 'old')
      self.db.entry_keyword_add(entry, 'station')
