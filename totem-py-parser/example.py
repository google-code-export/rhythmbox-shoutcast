"""
    totem-py-parser python library wrapper around totem-pl-parser.
    Copyright (C) 2009  Alexey Kuznetsov <ak@axet.ru>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import totem_py_parser

def pl_entry(parser, uri, htable):
  print 'uri: ' + uri
  print 'title: ' + htable.lookup('title').__str__()
  print 'genre: ' + htable.lookup('genre').__str__()

def parse_uri(uri):
  parser = totem_py_parser.TotemPyParser()
  parser.connect('entry-py-parsed', pl_entry)
  #g_object_set (parser, "recurse", FALSE, NULL);

  res = parser.parse(uri, False)
  
  return res

print parse_uri('http://yp.shoutcast.com/sbin/tunein-station.pls?id=9492')
