#!/usr/bin/env python

import os
import sys
import unittest


sys.path.insert(0, os.path.abspath(os.path.join(*[os.path.realpath(__file__), "..", "..", "sushi-bargain"])))
from address import *


test_addresses = [
    ("9-13 Cowcross Street, Farringdon, LONDON, UK, EC1M 6DR", "EC1M6DR"),
    ("77 Aldgate High Street, LONDON,  EC3N 1BD", "EC3N1BD"),
    ("47 King's Road, LONDON, SW3 4NB", "SW34NB"),
    ("Unit ASD6, Terminal Building, Stansted Airport, ESSEX, CM24 1RW", "CM241RW")
]

class AddressTest(unittest.TestCase):


    def test_extraction(self):
        for test_address in test_addresses:
            address_str, post_code = test_address
            address = Address(address_str)
            self.assertEquals(post_code, address.post_code(), "Did not properly extract post code")


    def test_raises_exception(self):
        with self.assertRaises(AddressException) as context:
            Address("bla bla").post_code()
        self.assertTrue('Could not extract post code from address: bla bla' in context.exception)


if __name__ == '__main__':
    unittest.main()