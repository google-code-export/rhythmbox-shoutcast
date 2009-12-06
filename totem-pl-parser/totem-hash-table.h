#ifndef TOTEM_HASH_TABLE_H
#define TOTEM_HASH_TABLE_H

#include <glib.h>

#include <gtk/gtk.h>

G_BEGIN_DECLS

#define TOTEM_TYPE_HASH_TABLE            (totem_hash_table_get_type ())
#define TOTEM_HASH_TABLE(obj)            (G_TYPE_CHECK_INSTANCE_CAST ((obj), TOTEM_TYPE_HASH_TABLE, TotemHashTable))
#define TOTEM_HASH_TABLE_CLASS(klass)    (G_TYPE_CHECK_CLASS_CAST ((klass), TOTEM_TYPE_HASH_TABLE, TotemHashTableClass))
#define TOTEM_IS_HASH_TABLE(obj)         (G_TYPE_CHECK_INSTANCE_TYPE ((obj), TOTEM_TYPE_HASH_TABLE))
#define TOTEM_IS_HASH_TABLE_CLASS(klass) (G_TYPE_CHECK_CLASS_TYPE ((klass), TOTEM_TYPE_HASH_TABLE))

typedef struct _TotemHashTablePrivate TotemHashTablePrivate;

typedef struct {
	GObject parent;

	TotemHashTablePrivate* private;
} TotemHashTable;

typedef struct {
	GObjectClass parent_class;
} TotemHashTableClass;

TotemHashTable *totem_hash_table_new (GHashTable *table);

const char* totem_hash_table_lookup (TotemHashTable *table, const char *key);

GType totem_hash_table_get_type(void);

G_END_DECLS

#endif /* TOTEM_PY_PARSER_H */
