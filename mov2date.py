#!/usr/bin/env python3

import sys
import os
import datetime
from pathlib import Path

class Mov2Date:
	def __init__(self, path):
		self.path = Path(path)

	def date(self):
		creation_time, _ = get_mov_timestamps(self.path)
		return creation_time

	def rename(self, prefix='', postfix=''):
		name = prefix + self.date().strftime("%Y%m%d_%H%M%S") + postfix
		new_path = self.path.with_name(name).with_suffix(self.path.suffix)
		print(new_path)
		os.rename(self.path, new_path)

def get_mov_timestamps(filename):
    ''' Get the creation and modification date-time from .mov metadata.

        Returns None if a value is not available.
    '''
    from datetime import datetime as DateTime
    import struct

    ATOM_HEADER_SIZE = 8
    # difference between Unix epoch and QuickTime epoch, in seconds
    EPOCH_ADJUSTER = 2082844800

    creation_time = modification_time = None

    # search for moov item
    with open(filename, "rb") as f:
        while True:
            atom_header = f.read(ATOM_HEADER_SIZE)
            #~ print('atom header:', atom_header)  # debug purposes
            if atom_header[4:8] == b'moov':
                break  # found
            else:
                atom_size = struct.unpack('>I', atom_header[0:4])[0]
                f.seek(atom_size - 8, 1)

        # found 'moov', look for 'mvhd' and timestamps
        atom_header = f.read(ATOM_HEADER_SIZE)
        if atom_header[4:8] == b'cmov':
            raise RuntimeError('moov atom is compressed')
        elif atom_header[4:8] != b'mvhd':
            raise RuntimeError('expected to find "mvhd" header.')
        else:
            f.seek(4, 1)
            creation_time = struct.unpack('>I', f.read(4))[0] - EPOCH_ADJUSTER
            creation_time = DateTime.fromtimestamp(creation_time)
            if creation_time.year < 1990:  # invalid or censored data
                creation_time = None

            modification_time = struct.unpack('>I', f.read(4))[0] - EPOCH_ADJUSTER
            modification_time = DateTime.fromtimestamp(modification_time)
            if modification_time.year < 1990:  # invalid or censored data
                modification_time = None

    return creation_time, modification_time

if __name__ == "__main__":
        if len(sys.argv) != 2:
                print("Usage: mov2date.py path/to/movie.mov")
        else:
                mov_path = sys.argv[1]
                m2d = Mov2Date(mov_path)
                m2d.rename(prefix='IMG_', postfix='')

