#include <string.h>
#include <glib.h>
#include <glib/gstdio.h>
#include <gio/gio.h>

void totempyparser_marshal_VOID__STRING_OBJECT (GClosure     *closure,
                                          GValue       *return_value G_GNUC_UNUSED,
                                          guint         n_param_values,
                                          const GValue *param_values,
                                          gpointer      invocation_hint G_GNUC_UNUSED,
                                          gpointer      marshal_data)
{
  typedef void (*GMarshalFunc_VOID__STRING_OBJECT) (gpointer     data1,
												   const gchar *     arg_1,
                                                   gpointer     arg_2,
                                                   gpointer     data2);
  register GMarshalFunc_VOID__STRING_OBJECT callback;
  register GCClosure *cc = (GCClosure*) closure;
  register gpointer data1, data2;

  g_return_if_fail (n_param_values == 3);

  if (G_CCLOSURE_SWAP_DATA (closure))
    {
      data1 = closure->data;
      data2 = g_value_peek_pointer (param_values + 0);
    }
  else
    {
      data1 = g_value_peek_pointer (param_values + 0);
      data2 = closure->data;
    }
  callback = (GMarshalFunc_VOID__STRING_OBJECT) (marshal_data ? marshal_data : cc->callback);

  callback (data1,
		  g_value_get_string (param_values + 1),
		  g_value_get_object (param_values + 2),
            data2);
}
