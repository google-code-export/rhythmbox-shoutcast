PYTHONVER = `python -c 'import sys; print sys.version[:3]'`
CFLAGS = `pkg-config --cflags gtk+-2.0 pygtk-2.0 totem-plparser` -fPIC -I/usr/include/python$(PYTHONVER) -I.
LDFLAGS = `pkg-config --libs gtk+-2.0 pygtk-2.0 totem-plparser`

all: totem_pl_parser.so

# Build the shared objects
totem_pl_parser.so: totem-pl-parser.o totem-pl-parser-module.o
	$(CC) $(LDFLAGS) -shared $^ -o $@

DEFS=`pkg-config --variable=defsdir pygtk-2.0`

totem-pl-parser.c: totem-pl-parser.def totem-pl-parser.override
	pygobject-codegen-2.0 --prefix totem_pl_parser \
	--register $(DEFS)/gdk-types.defs \
	--register $(DEFS)/gtk-types.defs \
	--override totem-pl-parser.override \
	totem-pl-parser.def > $@

clean:
	rm -f totem-pl-parser.c
	rm -f totem_pl_parser.so
