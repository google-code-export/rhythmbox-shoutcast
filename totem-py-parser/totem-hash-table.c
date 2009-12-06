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

#include <string.h>
#include <glib.h>
#include <glib/gstdio.h>
#include <gio/gio.h>

#include "totem-hash-table.h"

enum
{
  PROP_0,

  PROP_HASH_TABLE,
};

#define TOTEM_HASH_TABLE_GET_PRIVATE(obj) (G_TYPE_INSTANCE_GET_PRIVATE ((obj), TOTEM_TYPE_HASH_TABLE, TotemHashTablePrivate))

struct _TotemHashTablePrivate
{
  GHashTable *table;
};

static void totem_hash_table_class_init(TotemHashTableClass *klass);
static void totem_hash_table_init(TotemHashTable *parser);
static void totem_hash_table_finalize(GObject *object);

static void
totem_hash_table_set_property (GObject      *object,
                        guint         property_id,
                        const GValue *value,
                        GParamSpec   *pspec)
{
  TotemHashTable *self = TOTEM_HASH_TABLE (object);

  switch (property_id)
    {
    case PROP_HASH_TABLE:
      g_free (self->private->table);
      self->private->table = g_value_get_pointer(value);
      break;

    default:
      /* We don't have any other property... */
      G_OBJECT_WARN_INVALID_PROPERTY_ID (object, property_id, pspec);
      break;
    }
}

static void totem_hash_table_class_init(TotemHashTableClass *klass)
{
	g_type_class_add_private (klass, sizeof (TotemHashTablePrivate));

	GObjectClass *gobject_class = G_OBJECT_CLASS (klass);
	GParamSpec *pspec;

	gobject_class->set_property = totem_hash_table_set_property;

	pspec = g_param_spec_pointer ("hash-table",
							   "Base hash-table construct prop",
							   "Set hash table",
							   G_PARAM_CONSTRUCT_ONLY | G_PARAM_WRITABLE);
	g_object_class_install_property (gobject_class,
								   PROP_HASH_TABLE,
								   pspec);
}

TotemHashTable * totem_hash_table_new(GHashTable* hash)
{
	TotemHashTable *table = TOTEM_HASH_TABLE(g_object_new(TOTEM_TYPE_HASH_TABLE, "hash-table", hash, NULL));

	return table;
}

void totem_hash_table_init(TotemHashTable *table)
{
	TotemHashTablePrivate *priv;

	table->private = priv = TOTEM_HASH_TABLE_GET_PRIVATE (table);
}

const char* totem_hash_table_lookup (TotemHashTable *table, const char *key)
{
    const char* value = g_hash_table_lookup(table->private->table, key);

	return value;
}

G_DEFINE_TYPE (TotemHashTable, totem_hash_table, G_TYPE_OBJECT);
