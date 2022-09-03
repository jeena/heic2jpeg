heic2jpeg
=========

This script solves the problem that none of the browsers can show Apples HEIC pictures, many online services like Flickr don't allow their upload and it's also dificult to show them on the TV.

The solution is to transcode them into JPEG, but none of the tools available would copy all the EXIF data like "Date taken" or "Orientation" so that it is impossible to sort them and there is a lot of manual work involved to rotate them manually afterwards.

This script tries to copy as much metadata as necessary to avoid all the manual work.

Installation
------------

    git clone https://github.com/jeena/heic2jpeg.git
    sudo pacman -S perl-image-exiftool
    pipenv install
    pipenv shell

Usage
-----

    ./heic2jpeg.py original.heic
    
It will save the picture in the same directory, with the same name but as a JPEG and the ending `.jpg`.

    ./heic2date.py original.heic

This will get the date out of your .HEIC EXIF data and rename the file into IMG_YYYYMMDD_HHMMSS.heic

    ./mov2date.py original.mov

This will get the date out of your .mov file and rename the file into IMG_YYYYMMDD_HHMMSS.mov

You can automate it to do it for every specific file in a directory like this:

    find . -iname "*.HEIC" -exec ~/Projects/heic2jpeg/heic2date.py {} \;

License
-------

GPL v3
