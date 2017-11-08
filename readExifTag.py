import os
import PIL
from PIL import Image
from PIL.ExifTags import TAGS

fotodir = 'foto'


def get_field(exif, field):
    for (k, v) in exif.iteritems():
        if TAGS.get(k) == field:
            return v


print '---------------------------------------------------------------------------------'

for filename in os.listdir('foto'):
    print filename
    # print all tag informations
    for (k, v) in PIL.Image.open(fotodir + '/' + filename)._getexif().iteritems():
        print '%s = %s' % (TAGS.get(k), v)
    # or read a specific tag
    # print get_field(PIL.Image.open(fotodir + '/' + filename)._getexif(), 'DateTimeOriginal')
    print '---------------------------------------------------------------------------------'
