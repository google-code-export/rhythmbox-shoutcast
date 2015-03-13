# Introduction #

python bindings is part to connect two environment together: python and c code for example.

## direct calls ##

http://docs.python.org/library/dl.html

## ctypes ##

http://docs.python.org/library/ctypes.html

## gtk-objects ##

  * http://www.ibm.com/developerworks/linux/library/l-wrap/
  * http://faq.pygtk.org/index.py?req=show&file=faq19.017.htp
  * [Exporting a C API](http://library.gnome.org/devel/gobject/unstable/ch01s02.html)

bugreport about GHashTable gobject.GBoxed.
https://bugzilla.gnome.org/show_bug.cgi?id=412210
explain why unable to use GHashTable within python. (it probably already fixed in
last pygobject. check http://live.gnome.org/PyGObject)

### how to create .def stub ###

python /usr/share/pygobject/2.0/codegen/h2def.py /usr/include/totem-pl-parser/1/plparser/totem-pl-parser.h > totem-pl-parser.def

### how to create .c from .def ###
pygobject-codegen-2.0