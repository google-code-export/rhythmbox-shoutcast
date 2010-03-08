import rhythmdb
import xml.sax, xml.sax.handler

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
      
      track_url = 'http://yp.shoutcast.com/sbin/newxml.phtml?genre=%s' % genre
      
      entry = self.db.entry_lookup_by_location(track_url)
      if entry == None:
      	entry = self.db.entry_new(self.entry_type, track_url)

        if not entry:
          raise Exception('Unable to add entry to database')
        
        print "New genre: " + genre

      self.db.set(entry, rhythmdb.PROP_GENRE, genre)
      self.db.entry_keyword_remove(entry, 'old')
      self.db.entry_keyword_add(entry, 'genre')
