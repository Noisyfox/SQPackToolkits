#!/usr/bin/env python3

# ===============================================================
# This script read TEXT_XXXX from workspace/text_names.txt,
# and generate exh & exd names.
# ===============================================================
import re

from ffxiv_crc import compute_crc


def name2hash(name):
    crc = compute_crc(bytearray(name.lower(), encoding='ascii'))
    return format(crc, '04x')


if __name__ == '__main__':
    with open('workspace/text_names.txt', 'r') as f:
        TEXTs = f.readlines()

    pat1 = re.compile(r'\ATEXT_([0-9A-Z]+?)_(\d{5})(?:|_.*)\Z')
    pat2 = re.compile(r'\ATEXT_([0-9A-Z]+?)(?:|_.*)\Z')

    exh_set = set()
    base_name = None
    for t in TEXTs:
        t = t.strip()
        m = pat1.match(t)
        if m:
            base_name = '%s_%s' % (m.group(1).lower(), m.group(2).lower())
        else:
            m = pat2.match(t)
            if m:
                base_name = m.group(1).lower()
            else:
                base_name = None
                print("Can't parse name %s" % t)

        if base_name:
            exh_set.add('%s.exh' % base_name)
            exh_set.add('%s_0_de.exd' % base_name)
            exh_set.add('%s_0_en.exd' % base_name)
            exh_set.add('%s_0_fr.exd' % base_name)
            exh_set.add('%s_0_ja.exd' % base_name)
            exh_set.add('%s_0_chs.exd' % base_name)

    exh_list = list(exh_set)
    exh_list.sort()

    with open('workspace/exh_names.txt', 'w') as f:
        for n in exh_list:
            h = name2hash(n)
            f.write("%s %s\n" % (n, h))
