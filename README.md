# ImageDateFixer


Use dateFixer.py to modify creation date on the file based on the real creation date bring from exif tag of jpg.
This python script run only on macOsX using the "SetFile" command form xCode.

    usage: dateFixer.py [-h] [--dry-run] folder
    
    positional arguments:
      folder      Path to folder to scan for images
    
    optional arguments:
      -h, --help  show this help message and exit
      --dry-run   Noop, no change on files will be done


Use readExifTax.py to print tag from file on a specific folder.

(see inside the scripts for configuration)

Code inspired from:
http://bastibe.de/2015-10-03-changing-file-creation-dates.html

https://stackoverflow.com/questions/4764932/in-python-how-do-i-read-the-exif-data-for-an-image 

https://srcco.de/posts/writing-python-command-line-scripts.html