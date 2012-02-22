#!/bin/bash
# Hopefully gets the lyrics of all the Radiohead songs.
# Thanks to Green Plastic Radiohead for hosting them.

echo "Getting the lyrics index page"
curl http://www.greenplastic.com/radiohead-lyrics/ > index.html

# grab all the urls of the lyrics pages
sed -n 's|.*\(http://www.greenplastic.com/radiohead-lyrics/[^"]\+\)">.*|\1|p' index.html > urls.txt

# for each url, grab that page and pull out the lyrics
# well okay I was going to try this all in shell script, but python is easier:
python get_lyrics.py
