#!/usr/bin/env python3

import sys
import os
import datetime
import io
import pyheif
import piexif
from pathlib import Path

class Heic2Date:
	def __init__(self, path):
		self.path = Path(path)
		self.img = None

	def exif(self):
		himage = pyheif.read_heif(self.path)
		for metadata in himage.metadata or []:
			if metadata['type'] == 'Exif':
				return piexif.load(metadata['data'])

	def date(self):
                exif = self.exif()["Exif"]
                date_time_original = exif[piexif.ExifIFD.DateTimeOriginal].decode('utf-8')
                offset_time_original = exif[piexif.ExifIFD.OffsetTimeOriginal].decode('utf-8')
                dto = date_time_original + offset_time_original
                return datetime.datetime.strptime(dto, "%Y:%m:%d %H:%M:%S%z")
			
	def rename(self, prefix='', postfix=''):
		with open(self.path, 'rb') as image:
			name = prefix + self.date().strftime("%Y%m%d_%H%M%S") + postfix
			new_path = self.path.with_name(name).with_suffix(self.path.suffix)
			print(new_path)
			os.rename(self.path, new_path)

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print("Usage: heic2date.py path/to/picture.heic")
	else:
		img_path = sys.argv[1]
		h2d = Heic2Date(img_path)
		h2d.rename(prefix='IMG_', postfix='')
