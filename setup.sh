#!/bin/bash
# rhythmbox-shoutcast plugin for rhythmbox application.
# Copyright (C) 2009  Alexey Kuznetsov <ak@axet.ru>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

install() {
	# gedit plugin directory
	DEST=~/.gnome2/rhythmbox/plugins/shoutcast/
	SOURCE=$(dirname $0)

	# remove currect version of plugin
	rm -rf ${DEST}

	# create it
	mkdir -p ${DEST}

	# install currect verion of plugin
	cp -rv ${SOURCE}/plugin/* ${DEST}
}

uninstall() {
	# gedit plugin directory
	DEST=~/.gnome2/rhythmbox/plugins/shoutcast/

	# remove currect version of plugin
	rm -rf ${DEST}
}

# clean shoutcast cache
cleanc() {
	rm -vf ~/.cache/rhythmbox/shoutcast/*
}

# clean rhythmbox database (rhythmdb)
cleandb() {
	rm -vf ~/.local/share/rhythmbox/rhythmdb.xml 
}

# clean all rhythmdb settings
clean() {
	cleanc
	cleandb
}

case "$1" in
	clean)
		clean
		;;
	cleandb)
		cleandb
		;;
	cleanc)
		cleanc
		;;
	debug)
		install
		rhythmbox --rhythmdb-file=./../database.xml -D shoutcast
		;;
	help)
		echo $"Usage: $0 {clean|cleandb|cleanc|install|debug}"
		;;
	uninstall)
		uninstall
		;;
	install)
		install
		;;
	*)
		install
		;;
esac

exit 0
