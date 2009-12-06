//    totem-py-parser python library wrapper around totem-pl-parser.
//    Copyright (C) 2009  Alexey Kuznetsov <ak@axet.ru>
//
//    This program is free software: you can redistribute it and/or modify
//    it under the terms of the GNU General Public License as published by
//    the Free Software Foundation, either version 3 of the License, or
//    (at your option) any later version.
//
//    This program is distributed in the hope that it will be useful,
//    but WITHOUT ANY WARRANTY; without even the implied warranty of
//    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//    GNU General Public License for more details.
//
//    You should have received a copy of the GNU General Public License
//    along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
