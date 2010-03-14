import rhythmdb

import xml.sax, xml.sax.handler, datetime, urllib

import debug

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

class XmlStationsHandler(xml.sax.handler.ContentHandler):

  def __init__(self, db, entry_type, genre):
    xml.sax.handler.ContentHandler.__init__(self)
    self.db = db
    self.entry_type = entry_type
    self.genre = genre

  def startElement(self, name, attrs):
    self.attrs = attrs

  def endElement(self, name):
    if name == 'station':
      
      genre = self.genre
      id = int(self.attrs['id'])
      title = self.attrs['name']
      
      track_url = 'http://yp.shoutcast.com/sbin/tunein-station.pls?id=%d&genre=%s' % (id, urllib.quote(genre))
      track_url = urllib.quote(track_url)
      
      entry = self.db.entry_lookup_by_location (track_url)
      if entry == None:
      	entry = self.db.entry_new(self.entry_type, track_url)
        debug.log("New station: " + title)

      self.db.set(entry, rhythmdb.PROP_TITLE, title)
      self.db.set(entry, rhythmdb.PROP_GENRE, genre)
      self.db.entry_keyword_remove(entry, 'old')
      self.db.entry_keyword_add(entry, 'station')
