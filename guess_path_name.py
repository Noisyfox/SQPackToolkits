#!/usr/bin/env python3

# ===============================================================
# This script reads the hashes in workspace/path_guess_hashes.txt
# and try guessing the original path of them. The results are
# written to workspace/paths.txt
# ===============================================================
from typing import List

from ffxiv_crc import compute_crc


class NumberedRule:
    def __init__(self, pattern: str, start: int = 0, end: int = 100, digits: int = 3):
        self.pattern = pattern
        self.start = start
        self.end = end
        self.digits = digits

    def __iter__(self):
        return NumberedRuleIterator(self)


class NumberedRuleIterator:
    def __init__(self, rule: NumberedRule):
        self._rule = rule
        self._index = rule.start

    def __next__(self) -> str:
        if self._index > self._rule.end:
            raise StopIteration

        d = str(self._index)
        self._index += 1

        if len(d) < self._rule.digits:
            d = '0' * (self._rule.digits - len(d)) + d
        return self._rule.pattern.format(d)


rules = [
    NumberedRule('exd/custom/{}'),
    NumberedRule('exd/cut_scene/{}'),
    NumberedRule('exd/quest/{}'),
    NumberedRule('exd/dungeon/{}'),
    NumberedRule('game_script/custom/{}'),
    NumberedRule('game_script/quest/{}'),
]

if __name__ == '__main__':
    with open('workspace/path_guess_hashes.txt', 'r') as f:
        hashes = set([line.strip() for line in f.readlines()])

    results: List[str] = list()

    for rule in rules:
        for path in rule:
            crc = compute_crc(bytearray(path, encoding='ascii'))
            crc_hex = format(crc, '04x')

            if crc_hex in hashes:
                results.append('%s %s' % (path, crc_hex))
                hashes.remove(crc_hex)

    with open('workspace/paths.txt', 'w') as f:
        for n in results:
            f.write(n)
            f.write('\n')
