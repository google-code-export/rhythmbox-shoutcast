#include <pygobject.h>

void totem_pl_parser_add_constants(PyObject *module, const gchar *strip_prefix);
void totem_pl_parser_register_classes(PyObject *d);
extern PyMethodDef totem_pl_parser_functions[];

DL_EXPORT(void) inittotem_pl_parser(void)
{
  PyObject *m, *d;

  init_pygobject();

  m = Py_InitModule("totem_pl_parser", totem_pl_parser_functions);
  d = PyModule_GetDict(m);

  totem_pl_parser_register_classes(d);
  if(PyErr_Occurred()){
    Py_FatalError ("can't initialise module totem_pl_parser");
  }

  totem_pl_parser_add_constants(m, "");
}

