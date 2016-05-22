#!/usr/bin/env python

import os
import sys
import unittest


sys.path.insert(0, os.path.abspath(os.path.join(*[os.path.realpath(__file__), "..", "..", "sushi-bargain"])))
from postcode import *

test_csv_data = """id,postcode,latitude,longitude
1,AB10 1XG,57.144165160000000,-2.114847768000000
2,AB10 6RN,57.137879760000000,-2.121486688000000
3,AB10 7JB,57.124273770000000,-2.127189644000000
4,AB11 5QN,57.142701090000000,-2.093014619000000
5,AB11 6UL,57.137546630000000,-2.112695886000000
6,AB11 8RQ,57.135977620000000,-2.072114784000000
7,AB12 3FJ,57.098002900000000,-2.077668775000000
8,AB12 4NA,57.064272750000000,-2.130018015000000
9,AB12 5GL,57.081937920000000,-2.246567389000000"""


class PostCodeTest(unittest.TestCase):


    def test_line_parsing(self):
        test_csv_data_lines = [l.strip() for l in test_csv_data.splitlines()]
        table = construct_lookup_table(csv_data=test_csv_data_lines)
        self.assertEquals(9, len(table.keys()), "Wrong number of keys in lookup table")
        self.assertEquals(table["AB118RQ"], Position(longitude=-2.072114784, latitude=57.13597762), "Wrong look up for key")


if __name__ == '__main__':
    unittest.main()