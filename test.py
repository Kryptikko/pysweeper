# hello

import unittest

from init import lay_mines, build_map, lay_mine_markers
k
class TestMagic(unittest.TestCase):

    def test_build_map(self):
        map = build_map(5, 5)
        assert(len(map), 5)
        assert(len(map[0]), 5)
