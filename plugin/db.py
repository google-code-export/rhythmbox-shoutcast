import rhythmdb, rb

def id_to_entry(db, eid):
  entry = db.entry_lookup_by_id(eid)
  
  if not entry:
    raise Exception('iter_to_entry: bad entry ' + repr(eid) + ' ' + repr(id))

  return entry

def entry_to_id(db, entry):
  eid = db.entry_get(entry, rhythmdb.PROP_ENTRY_ID)

  return eid

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