#!/bin/sh
#
# $Id$
#
# This script is run as root before showing login widget.

xsetroot -solid rgb:255/8/8
rm /tmp/background.jpg
while [ \! -d /afs/dcti.sut.ru/media/wallpapers/xdm ];do
	sleep 1
done
count=`ls -1 /afs/dcti.sut.ru/media/wallpapers/xdm | wc -l`
rand=1`date +%N`
num=$((rand%count))
convert /afs/dcti.sut.ru/media/wallpapers/xdm/${num}.jpg -quality 100 /tmp/background.jpg

