#!/usr/bin/python
# coding: utf-8

import urllib2
import re
import time

outfile = open('all_lyrics.txt', 'w')
# for url in ['http://www.greenplastic.com/radiohead-lyrics/b-sides-and-other-non-album-songs/i-want-none-of-this/', 'http://www.greenplastic.com/radiohead-lyrics/b-sides-and-other-non-album-songs/lull/']:
songs = 0
for url in open('urls.txt'):
    url = url.strip()
    html = urllib2.urlopen(url).read()
    # it's a big string
    # "google_ad_section_start" comes before the lyrics and "SONG INFORMATION"
    # comes soon after, so chop off everything before/after that
    html = re.sub('.*google_ad_section_start -->(.*)SONG INFORMATION.*', '\\1',\
           html, flags=re.DOTALL)

    # strip out all html tags, we just want the text
    lyrics = re.sub('<.*?>', '', html)
    # a little cleanup
    lyrics = re.sub('&nbsp;', '', lyrics)
    lyrics = re.sub('&amp;', '&', lyrics)
    lyrics = re.sub('&#8217;', '\'', lyrics)
    lyrics = re.sub('&#8230;', '...', lyrics)
    lyrics = re.sub('&#8221;', '"', lyrics)
    lyrics = re.sub('&#8220;', '"', lyrics)
    lyrics = re.sub('&#8216;', '\'', lyrics)
    #8212 is a line of some kind; just punctuation, don't need it
    lyrics = re.sub('&#8212;', '', lyrics)
    #8211, the might em dash
    lyrics = re.sub('&#8211;', '-', lyrics)
    lyrics = re.sub('’', '\'', lyrics)
    # non breaking space, unicode 0xc2 0xa0
    lyrics = lyrics.replace('\xc2\xa0', ' ')

    outfile.write(lyrics)

    # don't want to wallop Green Plastic Radiohead
    time.sleep(1)

    songs += 1
    if not (songs % 10):
        print 'got this many songs: ' + str(songs)

