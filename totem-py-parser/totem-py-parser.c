#include <string.h>
#include <glib.h>
#include <glib/gstdio.h>
#include <gio/gio.h>

#include "totem-pl-parser.h"
#include "totem-py-parser.h"
#include "totem-disc.h"
#include "totem-hash-table.h"

#include "totem-py-parser-marshal.h"

#define TOTEM_PY_PARSER_GET_PRIVATE(obj) (G_TYPE_INSTANCE_GET_PRIVATE ((obj), TOTEM_TYPE_PY_PARSER, TotemPyParserPrivate))

enum
{
	ENTRY_PARSED,
	PLAYLIST_STARTED,
	PLAYLIST_ENDED,
	LAST_SIGNAL
};

struct _TotemPyParserPrivate
{
  TotemPlParser *pl;
};

static int totem_py_parser_table_signals[LAST_SIGNAL];

static void totem_py_parser_class_init(TotemPyParserClass *klass);
static void totem_py_parser_init(TotemPyParser *parser);
static void totem_py_parser_finalize(GObject *object);

static void totem_py_parser_entry_parsed(TotemPlParser *parser, const char *uri, GHashTable* metadata, TotemPyParser* py_parser);
static void totem_py_parser_playlist_started(TotemPlParser *parser, const char *uri, GHashTable* metadata, TotemPyParser* py_parser);
static void totem_py_parser_playlist_end(TotemPlParser *parser, const char *playlist_uri, TotemPyParser* py_parser);

static void totem_py_parser_class_init(TotemPyParserClass *klass)
{
	g_type_class_add_private (klass, sizeof (TotemPyParserPrivate));

	totem_py_parser_table_signals[ENTRY_PARSED] = g_signal_new("entry-py-parsed",
			G_TYPE_FROM_CLASS(klass), G_SIGNAL_RUN_LAST, 0, NULL, NULL,
					totempyparser_marshal_VOID__STRING_OBJECT, G_TYPE_NONE, 2,
			G_TYPE_STRING, TOTEM_TYPE_HASH_TABLE);

	totem_py_parser_table_signals[PLAYLIST_STARTED] = g_signal_new(
			"playlist-py-started", G_TYPE_FROM_CLASS(klass), G_SIGNAL_RUN_LAST,
			0, NULL, NULL,
			totempyparser_marshal_VOID__STRING_OBJECT, G_TYPE_NONE, 2,
			G_TYPE_STRING, G_TYPE_OBJECT);

	totem_py_parser_table_signals[PLAYLIST_ENDED] = g_signal_new(
			"playlist-py-ended", G_TYPE_FROM_CLASS(klass), G_SIGNAL_RUN_LAST,
			0, NULL, NULL,
			g_cclosure_marshal_VOID__STRING, G_TYPE_NONE, 1, G_TYPE_STRING);
}

TotemPyParser * totem_py_parser_new(void)
{
	TotemPyParser *parser = TOTEM_PY_PARSER(g_object_new(TOTEM_TYPE_PY_PARSER, NULL));

	return parser;
}

void totem_py_parser_init(TotemPyParser *parser)
{
	TotemPyParserPrivate *priv;

	parser->private = priv = TOTEM_PY_PARSER_GET_PRIVATE (parser);

	priv->pl = totem_pl_parser_new();

	g_signal_connect_data (G_OBJECT (priv->pl), "entry-parsed",
			       G_CALLBACK (totem_py_parser_entry_parsed),
			       parser, NULL, 0);
}

void totem_py_parser_entry_parsed(TotemPlParser *parser, const char *uri,
		GHashTable* metadata, TotemPyParser* py_parser)
{
	TotemHashTable *h = totem_hash_table_new(metadata);

	g_signal_emit(G_OBJECT(py_parser),
			totem_py_parser_table_signals[ENTRY_PARSED], 0, uri,
			h);
}

void totem_py_parser_playlist_started(TotemPlParser *parser, const char *uri,
		GHashTable* metadata, TotemPyParser* py_parser)
{
	TotemHashTable *h = totem_hash_table_new(metadata);

	g_signal_emit(G_OBJECT(parser),
			totem_py_parser_table_signals[PLAYLIST_STARTED], 0, uri,
			h);
}

void totem_py_parser_playlist_end(TotemPlParser *parser,
		const char *playlist_uri, TotemPyParser* py_parser)
{
	g_signal_emit(G_OBJECT(parser),
			totem_py_parser_table_signals[PLAYLIST_ENDED], 0, playlist_uri);
}

TotemPlParserResult
totem_py_parser_parse (TotemPyParser *parser, const char *uri,
		       gboolean fallback)
{
	return totem_pl_parser_parse (parser->private->pl, uri,  fallback);
}

G_DEFINE_TYPE (TotemPyParser, totem_py_parser, G_TYPE_OBJECT);
