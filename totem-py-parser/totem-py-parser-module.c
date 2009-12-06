#include <pygobject.h>

extern PyMethodDef totem_pl_parser_functions[];

void totem_pl_parser_add_constants(PyObject *module, const gchar *strip_prefix);
void totem_pl_parser_register_classes(PyObject *d);

DL_EXPORT(void) inittotem_py_parser(void)
{
  PyObject *m, *d;

  init_pygobject();

  m = Py_InitModule("totem_py_parser", totem_pl_parser_functions);
  d = PyModule_GetDict(m);

  totem_pl_parser_register_classes(d);
  if(PyErr_Occurred()){
    Py_FatalError ("can't initialise module totem_pl_parser");
  }

  totem_pl_parser_add_constants(m, "");
}
