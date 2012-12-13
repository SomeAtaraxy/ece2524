#!/bin/bash

while (($# == 1))
do
	wget -qO file1.html $*
	sed -e :a -e 's/<[^>]*>//g;/</N;//ba' file1.html > file1
	sleep 2
	wget -qO file2.html $*
	sed -e :a -e 's/<[^>]*>//g;/</N;//ba' file2.html > file2
	diff -yW 80 --suppress-common-lines file1 file2 | sed -e 's/\s\+|\s\+/  >  /g'
	echo
done

echo Usage: $0 [URL]
