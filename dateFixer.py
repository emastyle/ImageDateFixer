import logging
from argparse import ArgumentParser
import os,sys
import PIL
import datetime
from PIL import Image
from PIL.ExifTags import TAGS

ExifDateTag = 'DateTimeOriginal'


def get_field(exif,field):
    for (k,v) in exif.iteritems():
        if TAGS.get(k) == field:
            return v


def main(args):

    ExifDateTag = 'DateTimeOriginal'

    fotodir = args.folder

    if args.dry_run:
        print '--- dry-run mode, no file will be change ---'

    for filename in os.listdir(fotodir):

        print 'File : ' + filename

        t = datetime.datetime.fromtimestamp(os.path.getmtime(fotodir + '/' + filename))
        tnotime = datetime.datetime(t.year, t.month, t.day, 0, 0, 0)
        print 'File Creation Time: %s' % t

        exifcreatedate = get_field(PIL.Image.open(fotodir + '/' + filename)._getexif(), ExifDateTag)
        exifdatenotime = None

        if exifcreatedate is not None:
            exifcreatedateString = datetime.datetime.strptime(exifcreatedate, '%Y:%m:%d %H:%M:%S')
            exifdatenotime = datetime.datetime(exifcreatedateString.year, exifcreatedateString.month, exifcreatedateString.day, 0, 0, 0)

        print 'Exif ' + ExifDateTag + ': %s' % exifcreatedate

        if exifcreatedate is not None and tnotime != exifdatenotime:
            print 'Date differs, so change File Creation Time equal to ' + ExifDateTag

            if args.dry_run is False:
                d = datetime.datetime.strptime(exifcreatedate, '%Y:%m:%d %H:%M:%S')
                print 'Change file creation time and modification time to %s' % d
                # set the creation time
                os.system('SetFile -m "{}" {}'.format(d.strftime('%m/%d/%Y %H:%M:%S'), fotodir + '/' + filename))
                # set the file "modification time"
                os.system('SetFile -d "{}" {}'.format(d.strftime('%m/%d/%Y %H:%M:%S'), fotodir + '/' + filename))

        print '---------------------------------------------------------------------'


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', help='Noop, do not write anything', action='store_true')
    parser.add_argument('folder', help='Path to folder to scan for images')
    args = parser.parse_args()
    main(args)
