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
import xml.sax, xml.sax.handler, urllib
import debug, rbdb

class XmlGenresHandler(xml.sax.handler.ContentHandler):
  
  def __init__(self, db, entry_type):
  	xml.sax.handler.ContentHandler.__init__(self)
  	self.db = db
  	self.entry_type = entry_type
  
  def startElement(self, name, attrs):
  	self.attrs = attrs

  def endElement(self, name):
    if name == "genre":
      
      genre = self.attrs['name']
      
      track_url = 'http://yp.shoutcast.com/sbin/newxml.phtml?genre=%s' % (urllib.quote(genre))

      entry = rbdb.entry_lookup_by_location(self.db, track_url)
      if entry == None:
      	entry = self.db.entry_new(self.entry_type, track_url)        
        debug.log("New genre: " + genre)

      self.db.set(entry, rhythmdb.PROP_GENRE, genre)
      self.db.entry_keyword_remove(entry, 'old')
      self.db.entry_keyword_add(entry, 'genre')
