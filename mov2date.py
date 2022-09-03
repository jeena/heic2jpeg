#!/usr/bin/env python3

import sys
import os
import datetime
from pathlib import Path
from datetime import datetime
import subprocess

class Mov2Date:
	def __init__(self, path):
		self.path = Path(path)

	def date(self):
                result = subprocess.check_output(['exiftool', '-time:CreationDate', str(self.path)]).decode('utf-8')
                return datetime.strptime(result, "Creation Date                   : %Y:%m:%d %H:%M:%S%z\n")

	def rename(self, prefix='', postfix=''):
		name = prefix + self.date().strftime("%Y%m%d_%H%M%S") + postfix
		new_path = self.path.with_name(name).with_suffix(self.path.suffix)
		print(new_path)
		os.rename(self.path, new_path)
                
                
if __name__ == "__main__":
        if len(sys.argv) != 2:
                print("Usage: mov2date.py path/to/movie.mov")
        else:
                mov_path = sys.argv[1]
                m2d = Mov2Date(mov_path)
                m2d.rename(prefix='IMG_', postfix='')

