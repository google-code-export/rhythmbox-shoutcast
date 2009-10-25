/* -- THIS FILE IS GENERATED - DO NOT EDIT *//* -*- Mode: C; c-basic-offset: 4 -*- */

#include <Python.h>



#line 3 "totem-pl-parser.override"
#include "pygobject.h"
#include "totem-pl-parser.h"
#line 11 "totem-pl-parser.c"


/* ---------- types from other modules ---------- */
static PyTypeObject *_PyGObject_Type;
#define PyGObject_Type (*_PyGObject_Type)


/* ---------- forward type declarations ---------- */
PyTypeObject G_GNUC_INTERNAL PyTotemPlParser_Type;

#line 22 "totem-pl-parser.c"



/* ----------- TotemPlParser ----------- */

static int
_wrap_totem_pl_parser_new(PyGObject *self, PyObject *args, PyObject *kwargs)
{
    static char* kwlist[] = { NULL };

    if (!PyArg_ParseTupleAndKeywords(args, kwargs,
                                     ":totem_pl_parser.TotemPlParser.__init__",
                                     kwlist))
        return -1;

    pygobject_constructv(self, 0, NULL);
    if (!self->obj) {
        PyErr_SetString(
            PyExc_RuntimeError, 
            "could not create totem_pl_parser.TotemPlParser object");
        return -1;
    }
    return 0;
}

static PyObject *
_wrap_totem_pl_parser_add_ignored_scheme(PyGObject *self, PyObject *args, PyObject *kwargs)
{
    static char *kwlist[] = { "scheme", NULL };
    char *scheme;

    if (!PyArg_ParseTupleAndKeywords(args, kwargs,"s:TotemPlParser.add_ignored_scheme", kwlist, &scheme))
        return NULL;
    
    totem_pl_parser_add_ignored_scheme(TOTEM_PL_PARSER(self->obj), scheme);
    
    Py_INCREF(Py_None);
    return Py_None;
}

static PyObject *
_wrap_totem_pl_parser_add_ignored_mimetype(PyGObject *self, PyObject *args, PyObject *kwargs)
{
    static char *kwlist[] = { "mimetype", NULL };
    char *mimetype;

    if (!PyArg_ParseTupleAndKeywords(args, kwargs,"s:TotemPlParser.add_ignored_mimetype", kwlist, &mimetype))
        return NULL;
    
    totem_pl_parser_add_ignored_mimetype(TOTEM_PL_PARSER(self->obj), mimetype);
    
    Py_INCREF(Py_None);
    return Py_None;
}

static PyObject *
_wrap_totem_pl_parser_parse(PyGObject *self, PyObject *args, PyObject *kwargs)
{
    static char *kwlist[] = { "uri", "fallback", NULL };
    char *uri;
    int fallback;
    gint ret;

    if (!PyArg_ParseTupleAndKeywords(args, kwargs,"si:TotemPlParser.parse", kwlist, &uri, &fallback))
        return NULL;
    
    ret = totem_pl_parser_parse(TOTEM_PL_PARSER(self->obj), uri, fallback);
    
    return pyg_enum_from_gtype(TOTEM_TYPE_PL_PARSER_RESULT, ret);
}

static PyObject *
_wrap_totem_pl_parser_parse_with_base(PyGObject *self, PyObject *args, PyObject *kwargs)
{
    static char *kwlist[] = { "uri", "base", "fallback", NULL };
    char *uri, *base;
    int fallback;
    gint ret;

    if (!PyArg_ParseTupleAndKeywords(args, kwargs,"ssi:TotemPlParser.parse_with_base", kwlist, &uri, &base, &fallback))
        return NULL;
    
    ret = totem_pl_parser_parse_with_base(TOTEM_PL_PARSER(self->obj), uri, base, fallback);
    
    return pyg_enum_from_gtype(TOTEM_TYPE_PL_PARSER_RESULT, ret);
}

static const PyMethodDef _PyTotemPlParser_methods[] = {
    { "add_ignored_scheme", (PyCFunction)_wrap_totem_pl_parser_add_ignored_scheme, METH_VARARGS|METH_KEYWORDS,
      NULL },
    { "add_ignored_mimetype", (PyCFunction)_wrap_totem_pl_parser_add_ignored_mimetype, METH_VARARGS|METH_KEYWORDS,
      NULL },
    { "parse", (PyCFunction)_wrap_totem_pl_parser_parse, METH_VARARGS|METH_KEYWORDS,
      NULL },
    { "parse_with_base", (PyCFunction)_wrap_totem_pl_parser_parse_with_base, METH_VARARGS|METH_KEYWORDS,
      NULL },
    { NULL, NULL, 0, NULL }
};

PyTypeObject G_GNUC_INTERNAL PyTotemPlParser_Type = {
    PyObject_HEAD_INIT(NULL)
    0,                                 /* ob_size */
    "totem_pl_parser.TotemPlParser",                   /* tp_name */
    sizeof(PyGObject),          /* tp_basicsize */
    0,                                 /* tp_itemsize */
    /* methods */
    (destructor)0,        /* tp_dealloc */
    (printfunc)0,                      /* tp_print */
    (getattrfunc)0,       /* tp_getattr */
    (setattrfunc)0,       /* tp_setattr */
    (cmpfunc)0,           /* tp_compare */
    (reprfunc)0,             /* tp_repr */
    (PyNumberMethods*)0,     /* tp_as_number */
    (PySequenceMethods*)0, /* tp_as_sequence */
    (PyMappingMethods*)0,   /* tp_as_mapping */
    (hashfunc)0,             /* tp_hash */
    (ternaryfunc)0,          /* tp_call */
    (reprfunc)0,              /* tp_str */
    (getattrofunc)0,     /* tp_getattro */
    (setattrofunc)0,     /* tp_setattro */
    (PyBufferProcs*)0,  /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,                      /* tp_flags */
    NULL,                        /* Documentation string */
    (traverseproc)0,     /* tp_traverse */
    (inquiry)0,             /* tp_clear */
    (richcmpfunc)0,   /* tp_richcompare */
    offsetof(PyGObject, weakreflist),             /* tp_weaklistoffset */
    (getiterfunc)0,          /* tp_iter */
    (iternextfunc)0,     /* tp_iternext */
    (struct PyMethodDef*)_PyTotemPlParser_methods, /* tp_methods */
    (struct PyMemberDef*)0,              /* tp_members */
    (struct PyGetSetDef*)0,  /* tp_getset */
    NULL,                              /* tp_base */
    NULL,                              /* tp_dict */
    (descrgetfunc)0,    /* tp_descr_get */
    (descrsetfunc)0,    /* tp_descr_set */
    offsetof(PyGObject, inst_dict),                 /* tp_dictoffset */
    (initproc)_wrap_totem_pl_parser_new,             /* tp_init */
    (allocfunc)0,           /* tp_alloc */
    (newfunc)0,               /* tp_new */
    (freefunc)0,             /* tp_free */
    (inquiry)0              /* tp_is_gc */
};



/* ----------- functions ----------- */

static PyObject *
_wrap_totem_pl_parser_parse_duration(PyObject *self, PyObject *args, PyObject *kwargs)
{
    static char *kwlist[] = { "duration", "debug", NULL };
    char *duration;
    int debug;
    gint64 ret;

    if (!PyArg_ParseTupleAndKeywords(args, kwargs,"si:totem_pl_parser_parse_duration", kwlist, &duration, &debug))
        return NULL;
    
    ret = totem_pl_parser_parse_duration(duration, debug);
    
    return PyLong_FromLongLong(ret);
}

static PyObject *
_wrap_totem_pl_parser_parse_date(PyObject *self, PyObject *args, PyObject *kwargs)
{
    static char *kwlist[] = { "date_str", "debug", NULL };
    char *date_str;
    int debug;
    guint64 ret;

    if (!PyArg_ParseTupleAndKeywords(args, kwargs,"si:totem_pl_parser_parse_date", kwlist, &date_str, &debug))
        return NULL;
    
    ret = totem_pl_parser_parse_date(date_str, debug);
    
    return PyLong_FromUnsignedLongLong(ret);
}

const PyMethodDef totem_pl_parser_functions[] = {
    { "totem_pl_parser_parse_duration", (PyCFunction)_wrap_totem_pl_parser_parse_duration, METH_VARARGS|METH_KEYWORDS,
      NULL },
    { "totem_pl_parser_parse_date", (PyCFunction)_wrap_totem_pl_parser_parse_date, METH_VARARGS|METH_KEYWORDS,
      NULL },
    { NULL, NULL, 0, NULL }
};


/* ----------- enums and flags ----------- */

void
totem_pl_parser_add_constants(PyObject *module, const gchar *strip_prefix)
{
#ifdef VERSION
    PyModule_AddStringConstant(module, "__version__", VERSION);
#endif
  pyg_enum_add(module, "PlParserResult", strip_prefix, TOTEM_TYPE_PL_PARSER_RESULT);
  pyg_enum_add(module, "PlParserType", strip_prefix, TOTEM_TYPE_PL_PARSER_TYPE);
  pyg_enum_add(module, "PlParserError", strip_prefix, TOTEM_TYPE_PL_PARSER_ERROR);

  if (PyErr_Occurred())
    PyErr_Print();
}

/* initialise stuff extension classes */
void
totem_pl_parser_register_classes(PyObject *d)
{
    PyObject *module;

    if ((module = PyImport_ImportModule("gobject")) != NULL) {
        _PyGObject_Type = (PyTypeObject *)PyObject_GetAttrString(module, "GObject");
        if (_PyGObject_Type == NULL) {
            PyErr_SetString(PyExc_ImportError,
                "cannot import name GObject from gobject");
            return ;
        }
    } else {
        PyErr_SetString(PyExc_ImportError,
            "could not import gobject");
        return ;
    }


#line 248 "totem-pl-parser.c"
    pygobject_register_class(d, "TotemPlParser", TOTEM_TYPE_PL_PARSER, &PyTotemPlParser_Type, Py_BuildValue("(O)", &PyGObject_Type));
    pyg_set_object_has_new_constructor(TOTEM_TYPE_PL_PARSER);
}
