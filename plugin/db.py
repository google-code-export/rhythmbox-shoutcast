import rhythmdb, rb

def iter_to_entry(db, model, iter):
  id = model.get(iter, 0)[0]
  if not id:
    raise Exception('Bad id' + id)
  eid = db.entry_get(id, rhythmdb.PROP_ENTRY_ID)
  if not eid:
    raise Exception('Bad eid' + eid)
  
  entry = db.entry_lookup_by_id(eid)
  
  if not entry:
    raise Exception('iter_to_entry: bad entry ' + repr(eid) + ' ' + repr(id))

  return entry