#!/usr/bin/env python3

# ======================================================================
# This script read file names and hashes from workspace/exh_names.txt,
# and workspace/paths.txt, and update workspace/hashlist.db
# ======================================================================
import os
import sqlite3
import struct
from typing import List, Tuple


def read_hashes(file_path: str) -> List[Tuple[str, int]]:
    if not os.path.exists(file_path):
        return []

    def split_name_hash(_ns):
        t = _ns.strip().split(' ')
        hash_int = int(t[1], 16)
        hash_int = struct.unpack_from('<i', struct.pack('<I', hash_int))[0]
        return t[0], hash_int

    with open(file_path, 'r') as f:
        lines = f.readlines()

    return [split_name_hash(line) for line in lines]


if __name__ == '__main__':
    path_hashes = read_hashes('workspace/paths.txt')
    name_hashes = read_hashes('workspace/exh_names.txt')

    with sqlite3.connect('workspace/hashlist.db') as db:
        # Update paths
        for p, h in path_hashes:
            v = db.execute('SELECT * FROM folders WHERE hash=?', (h,)).fetchone()
            if v:
                print("Find!")
            else:
                r = db.execute("INSERT INTO folders (hash, path, archive, version) VALUES (?,?,?,1)", (h, p, '-1'))
                pass

        # Update file names
        for n, h in name_hashes:
            v = db.execute('SELECT * FROM filenames WHERE hash=?', (h,)).fetchone()
            if v:
                print("Find!")
            else:
                r = db.execute("INSERT INTO filenames (hash, name, archive, version) VALUES (?,?,?,1)", (h, n, '-1'))
                pass
