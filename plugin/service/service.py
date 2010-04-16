import rhythmdb
import xml.sax, xml.sax.handler, shutil, os, os.path
import rbdb, debug

# one more check requred: items not marked as station or genre

def check_for_damage(db, entry_type):
  query = db.query_new()
  db.query_append(query, (rhythmdb.QUERY_PROP_EQUALS, rhythmdb.PROP_TYPE, entry_type))
  db.query_append(query, (rhythmdb.QUERY_PROP_LIKE, rhythmdb.PROP_KEYWORD, 'genre'))
  db.query_append(query, (rhythmdb.QUERY_PROP_LIKE, rhythmdb.PROP_KEYWORD, 'station'))
  query_model = db.query_model_new_empty()
  db.do_full_query_parsed(query_model, query)

  check = query_model.get_iter_first()
  return bool(check)

def check_and_serve(db, entry_type):
  if check_for_damage(db, entry_type):
    debug.log('Database damaged, clean ALL')
    delete_all(db, entry_type)

def delete_all(db, entry_type):
  db.entry_delete_by_type(entry_type)
