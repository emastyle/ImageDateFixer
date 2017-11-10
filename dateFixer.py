from argparse import ArgumentParser
import os,sys
import PIL
import datetime
from PIL import Image
from PIL.ExifTags import TAGS
import logging

ExifDateTag = 'DateTimeOriginal'


def get_field(exif,field):
    for (k,v) in exif.iteritems():
        if TAGS.get(k) == field:
            return v


def main(args):

    ExifDateTag = 'DateTimeOriginal'

    imgdir = args.folder

    logging.basicConfig(filename='dateFixer.log', level=args.loglevel or logging.DEBUG)

    logging.info('Starting the script %s..', sys.argv[0])

    if args.dry_run:
        logging.info('--- dry-run mode, no file will be change ---')
        #print '--- dry-run mode, no file will be change ---'

    for filename in os.listdir(imgdir):

        if filename.lower().endswith(('.jpg', '.jpeg')) is False:
            continue

        logging.info('File : %s', filename)

        t = datetime.datetime.fromtimestamp(os.path.getmtime(imgdir + '/' + filename))
        tnotime = datetime.datetime(t.year, t.month, t.day, 0, 0, 0)
        logging.info('File Creation Time: %s', t)

        exifcreatedate = get_field(PIL.Image.open(imgdir + '/' + filename)._getexif(), ExifDateTag)
        exifdatenotime = None

        if exifcreatedate is not None:
            exifcreatedateString = datetime.datetime.strptime(exifcreatedate, '%Y:%m:%d %H:%M:%S')
            exifdatenotime = datetime.datetime(exifcreatedateString.year, exifcreatedateString.month, exifcreatedateString.day, 0, 0, 0)

        logging.info('Exif ' + ExifDateTag + ': %s', exifcreatedate)

        if exifcreatedate is not None and tnotime != exifdatenotime:
            logging.info('Date differs, so change File Creation Time equal to %s', ExifDateTag)

            if args.dry_run is False:
                d = datetime.datetime.strptime(exifcreatedate, '%Y:%m:%d %H:%M:%S')
                logging.info('Change file creation time and modification time to %s', d)
                # set the creation time
                os.system('SetFile -m "{}" {}'.format(d.strftime('%m/%d/%Y %H:%M:%S'), imgdir + '/' + filename))
                # set the file "modification time"
                os.system('SetFile -d "{}" {}'.format(d.strftime('%m/%d/%Y %H:%M:%S'), imgdir + '/' + filename))
        else:
            logging.info('Nothing to do.')

        logging.info('---------------------------------------------------------------------')


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-v', '--verbose', help='Verbose (debug) logging', action='store_const', const=logging.info,
                       dest='loglevel')
    group.add_argument('-q', '--quiet', help='Silent mode, only log warnings', action='store_const',
                       const=logging.WARN, dest='loglevel')
    parser.add_argument('--dry-run', help='Noop, no change on files will be done', action='store_true')
    parser.add_argument('folder', help='Path to folder to scan for images')
    args = parser.parse_args()
    main(args)
