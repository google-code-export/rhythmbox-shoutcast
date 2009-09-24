import rhythmdb
import xml.sax, xml.sax.handler

class XmlGenreHandler(xml.sax.handler.ContentHandler):

	def __init__(self, db, entry_type):
		xml.sax.handler.ContentHandler.__init__(self)
		self.db = db
		self.entry_type = entry_type

	def startElement(self, name, attrs):
		self.attrs = attrs

	def endElement(self, name):
		if name == "genre":
			track_url = 'http://yp.shoutcast.com/sbin/newxml.phtml?genre=%s' % self.attrs['name']

			entry = self.db.entry_lookup_by_location (track_url)
			if entry == None:
				entry = self.db.entry_new(self.entry_type, track_url)

			self.db.set(entry, rhythmdb.PROP_GENRE, self.attrs['name'])
			self.db.entry_keyword_add(entry, 'new')

			self.db.commit()
