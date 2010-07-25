import rhythmdb, rb
import rbdb, debug, load
import StringIO, urllib, base64

from xml.sax import saxutils, make_parser, SAXParseException
from xml.sax.handler import feature_namespaces, feature_namespace_prefixes, ContentHandler
from xml.sax.saxutils import XMLGenerator
from xml.sax.xmlreader import AttributesImpl

import opml

class ShoutcastOPML(opml.OPML):

  def __init__(self):
    opml.OPML.__init__(self)
  
  def read(self, file):
    """ read opml from file into OPML object """
    f = open(file, 'r')

    parser = make_parser()
    parser.setFeature(feature_namespaces, 0)
    handler = opml.OPMLHandler()
    handler._opml = self
    parser.setContentHandler(handler)

    parser.parse(f)
    
  def save(self, db, data_dir, entry_type):
    """ save data to database """

    print self.outlines

    for outline in self.outlines:
      genre = outline['category']
      title = outline['text']
      track_url = outline['url']
      playlist = outline.get_playlist()

      genre_url = load.xmlgenres_encodeurl(genre)

      entry = rbdb.entry_lookup_by_location(db, genre_url)
      if entry == None:
        entry = db.entry_new(entry_type, genre_url)        
        debug.log("New genre: " + genre)
  
        db.set(entry, rhythmdb.PROP_GENRE, genre)
        db.entry_keyword_add(entry, 'genre')

      # at first we need to find any local favorite stations.
      # if it fount, do update all from OPML (title, playlist and other)
      url = load.playlist_filename_url(data_dir, track_url, title)
      entry = rbdb.entry_lookup_by_location(db, url)
      
      if entry == None:
        # if we don't.
        # try to look up same station TITLE+ID
        entry = rbdb.entry_lookup_by_location(db, track_url)
        if entry:
          title_db = db.entry_get(entry, rhythmdb.PROP_TITLE)
          if title != title_db:
            # if ID is the same but TITLE is different create the new entry
            entry = None

        if entry == None:
          entry = db.entry_new(entry_type, url)
          debug.log("New station: " + title)

      db.set(entry, rhythmdb.PROP_TITLE, title)
      db.set(entry, rhythmdb.PROP_GENRE, genre)
      db.entry_keyword_add(entry, 'station')
      db.entry_keyword_add(entry, 'star')
      
      if playlist:
        file = open(load.playlist_filename(data_dir, track_url, title), 'w')
        file.write(playlist)
      
    db.commit()

  def load(self, db, entry_type):
    self['title'] = 'Favorite stations'

    stations_query = db.query_new()
    db.query_append(stations_query, (rhythmdb.QUERY_PROP_EQUALS, rhythmdb.PROP_TYPE, entry_type))
    db.query_append(stations_query, (rhythmdb.QUERY_PROP_LIKE, rhythmdb.PROP_KEYWORD, 'station'))
    db.query_append(stations_query, (rhythmdb.QUERY_PROP_LIKE, rhythmdb.PROP_KEYWORD, 'star'))
    stations_query_model = db.query_model_new_empty ()
    db.do_full_query_parsed(stations_query_model, stations_query)
    stations_query_model.foreach(self.store, db)

  def store(self, model, path, iter, db):
    entry = rbdb.iter_to_entry(db, model, iter)

    outline = opml.Outline()
    outline['type'] = 'link'
    outline['text'] = db.entry_get(entry, rhythmdb.PROP_TITLE)
    outline['category'] = db.entry_get(entry, rhythmdb.PROP_GENRE)
    url = db.entry_get(entry, rhythmdb.PROP_LOCATION)
    if load.playlist_isfilename(url):
      filename = urllib.urlretrieve(url)[0]
      file = open(filename)
      playlist = file.read()
      outline.set_playlist(playlist)
      url = load.playlist_filename2url(url)
    outline['url'] = url
    self.outlines.append(outline)

  def xml(self):
    stream = StringIO.StringIO()
    self.output(stream)
    return stream.getvalue()
  
  def write(self, file):
    f = open(file, 'w')
    f.write(self.xml())
    f.close()
  