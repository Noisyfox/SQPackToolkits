#!/usr/bin/env python3

# ===============================================================
# This script can extract all string name from luab scripts
# ===============================================================
import re
import sys

import os
from typing import List, Set

if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise Exception('Missing path to extracted .luab files!')

    path = sys.argv[1]

    pat = re.compile(b'TEXT[_A-Z0-9]+?\0')
    text_set: Set[str] = set()
    for root, dirs, files in os.walk(path):
        for luab in files:
            with open(os.path.join(root, luab), 'rb') as f:
                s = f.read()
            all_names: List[bytes] = pat.findall(s)
            for text_name in all_names:
                text_name = text_name[:-1].decode('ascii') + '\n'
                text_set.add(text_name)

    text_list = list(text_set)
    text_list.sort()

    with open('workspace/text_names.txt', 'w') as f:
        f.writelines(text_list)
