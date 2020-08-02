#!/usr/bin/env python3

# ======================================================================
# This script read file names and hashes from workspace/exh_names.txt,
# and update workspace/hashlist.db
# ======================================================================
import sqlite3
import struct

if __name__ == '__main__':
    with open('workspace/exh_names.txt', 'r') as f:
        names = f.readlines()

    def split_name_hash(_ns):
        t = _ns.strip().split(' ')
        hash_int = int(t[1], 16)
        hash_int = struct.unpack_from('<i', struct.pack('<I', hash_int))[0]
        return t[0], hash_int

    name_hash = [split_name_hash(ns) for ns in names]

    with sqlite3.connect('workspace/hashlist.db') as db:
        for n, h in name_hash:
            v = db.execute('SELECT * FROM filenames WHERE hash=?', (h,)).fetchone()
            if v:
                print("Find!")
            else:
                r = db.execute("INSERT INTO filenames (hash, name, archive, version) VALUES (?,?,?,1)", (h, n, '-1'))
                pass
