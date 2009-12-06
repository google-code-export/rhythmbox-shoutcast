#ifndef TOTEM_PY_PARSER_H
#define TOTEM_PY_PARSER_H

#include <glib.h>

#include <gtk/gtk.h>
#include <totem-pl-parser-features.h>
#include <totem-pl-parser-builtins.h>

G_BEGIN_DECLS

#define TOTEM_TYPE_PY_PARSER            (totem_py_parser_get_type ())
#define TOTEM_PY_PARSER(obj)            (G_TYPE_CHECK_INSTANCE_CAST ((obj), TOTEM_TYPE_PY_PARSER, TotemPyParser))
#define TOTEM_PY_PARSER_CLASS(klass)    (G_TYPE_CHECK_CLASS_CAST ((klass), TOTEM_TYPE_PY_PARSER, TotemPyParserClass))
#define TOTEM_IS_PY_PARSER(obj)         (G_TYPE_CHECK_INSTANCE_TYPE ((obj), TOTEM_TYPE_PY_PARSER))
#define TOTEM_IS_PY_PARSER_CLASS(klass) (G_TYPE_CHECK_CLASS_TYPE ((klass), TOTEM_TYPE_PY_PARSER))

typedef struct _TotemPyParserPrivate TotemPyParserPrivate;

typedef struct {
	GObject parent;

	TotemPyParserPrivate* private;
} TotemPyParser;

typedef struct {
	GObjectClass parent_class;
} TotemPyParserClass;

TotemPyParser *totem_py_parser_new (void);

TotemPlParserResult totem_py_parser_parse (TotemPyParser *parser, const char *uri, gboolean fallback);

GType totem_py_parser_get_type(void);

G_END_DECLS

#endif /* TOTEM_PY_PARSER_H */
