import os,sys
import PIL
import datetime
from PIL import Image
from PIL.ExifTags import TAGS

fotodir = 'foto'


def get_field (exif,field) :
    for (k,v) in exif.iteritems():
        if TAGS.get(k) == field:
            return v


for filename in os.listdir('foto'):

    exifCreateDate = get_field(PIL.Image.open(fotodir + '/' + filename)._getexif(), 'DateTimeOriginal')

    if exifCreateDate != None :
        print 'Change date on file : ' + filename + ' to ' + exifCreateDate;
        d = datetime.datetime.strptime(exifCreateDate, '%Y:%m:%d %H:%M:%S')
        # set the file "modification time"
        os.system('SetFile -d "{}" {}'.format(d.strftime('%m/%d/%Y %H:%M:%S'), fotodir + '/' + filename))
        # set the creation time
        os.system('SetFile -m "{}" {}'.format(d.strftime('%m/%d/%Y %H:%M:%S'), fotodir + '/' + filename))

