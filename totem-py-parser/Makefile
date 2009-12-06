# Copyright (C) 2009  Alexey Kuznetsov <ak@axet.ru>

PYTHONVER = `python -c 'import sys; print sys.version[:3]'`
CFLAGS = `pkg-config --cflags gtk+-2.0 pygtk-2.0 totem-plparser` -fPIC -I/usr/include/python$(PYTHONVER) -I.
LDFLAGS = `pkg-config --libs gtk+-2.0 pygtk-2.0 totem-plparser`

all: totem_py_parser.so

# Build the shared objects
totem_py_parser.so: totem-pl-parser.o totem-py-parser-module.o totem-py-parser.o totem-py-parser-marshal.o totem-hash-table.o
	$(CC) $(LDFLAGS) -shared $^ -o $@

DEFS=`pkg-config --variable=defsdir pygtk-2.0`

totem-pl-parser.c: totem-py-parser.def totem-py-parser.override
	pygobject-codegen-2.0 --prefix totem_pl_parser \
	--register $(DEFS)/gdk-types.defs \
	--register $(DEFS)/gtk-types.defs \
	--override totem-py-parser.override \
	totem-py-parser.def > $@

clean:
	rm -f totem-pl-parser.c
	rm -f totem_py_parser.so
	rm -f *.o