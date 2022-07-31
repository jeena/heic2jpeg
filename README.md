heic2jpeg
=========

This script solves the problem that none of the browsers can show Apples HEIC pictures, many online services like Flickr don't allow their upload and it's also dificult to show them on the TV.

The solution is to transcode them into JPEG, but none of the tools available would copy all the EXIF data like "Date taken" or "Orientation" so that it is impossible to sort them and there is a lot of manual work involved to rotate them manually afterwards.

This script tries to copy as much metadata as necessary to avoid all the manual work.

Installation
------------

pipenv install
pipenv shell

Usage
-----

    ./heic2jpeg.py original.heic
    
It will save the picture in the same directory, with the same name but as a JPEG and the ending `.jpeg`.

