#!/usr/bin/env python3

import sys
import io
import pyheif
import piexif
from PIL import Image
from pathlib import Path

class Heic2Jpeg:
	def __init__(self, path):
		self.path = Path(path)
		self.img = None
	
	def decodeImage(self):
		self.himage = pyheif.read_heif(self.path)
		self.img = Image.frombytes(
			self.himage.mode,
			self.himage.size,
			self.himage.data,
			"raw",
			self.himage.mode,
			self.himage.stride)
			
	def getExif(self):
		for metadata in self.himage.metadata or []:
			if metadata['type'] == 'Exif':
				# pyheif.read_heif() rotates the picture
				# we need to remove the Orientation from EXIF
				exif_dict = piexif.load(metadata['data'])
				if exif_dict["0th"] and exif_dict["0th"][piexif.ImageIFD.Orientation]:
					exif_dict["0th"][piexif.ImageIFD.Orientation] = 1
					
				return piexif.dump(exif_dict)
		
	def safe(self, quality=85):
		if self.img == None:
			self.decodeImage()
			
		path = self.path.with_suffix('.jpg')

		self.img.save(
			path,
			format="JPEG",
			quality=quality,
			exif=self.getExif())
		return path.__str__()

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print("Usage: heic2jpeg.py path/to/picture.heic")
	else:
		img_path = sys.argv[1]
		h2j = Heic2Jpeg(img_path)
		print(h2j.safe())
