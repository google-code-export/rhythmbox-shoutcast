#!/bin/bash

DEST=~/.gnome2/rhythmbox/plugins/shoutcast/

mkdir -p ${DEST}

cp -v *.py ${DEST}
cp -v *.ui ${DEST}
cp -v *.png ${DEST}
cp -v *.rb-plugin ${DEST}

