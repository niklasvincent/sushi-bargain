#!/usr/bin/env python

import json
import unittest
from functools import reduce

from sushi_bargain.itsu import ItsuApi
from sushi_bargain.lookup import LookupGenerator


class TestLookupGenerator(unittest.TestCase):

    def test_times_to_time_slots(self):
        time_slots = LookupGenerator._times_to_time_slots([
            20.0,
            20.0,
            20.0,
            20.0,
            20.0,
            20.0,
            18.5
        ])
        self.assertEqual([40, 88, 136, 184, 232, 280, 325], time_slots)

    def test_time_slots_for_branches(self):
        branch_json = """{"branches": [{
            "title": "Leeds Commercial Street",
            "address_1": "36-38 Commercial Street",
            "address_2": "",
            "city": "Leeds",
            "state": "",
            "postal_code": "LS1 6EX",
            "country": "UK",
            "telephone": "0113-467-7592",
            "latitude": "53.797250",
            "longitude": "-1.544502",
            "transit_info": "",
            "wifi_available": true,
            "hours": [
              {
                "title": "Monday",
                "hours": "10am - 8.30pm",
                "highlight": false
              },
              {
                "title": "Tuesday",
                "hours": "10am - 8.30pm",
                "highlight": false
              },
              {
                "title": "Wednesday",
                "hours": "10am - 8.30pm",
                "highlight": false
              },
              {
                "title": "Thursday",
                "hours": "10am - 8.30pm",
                "highlight": false
              },
              {
                "title": "Friday",
                "hours": "10am - 8.30pm",
                "highlight": false
              },
              {
                "title": "Saturday",
                "hours": "10am - 8.30pm",
                "highlight": false
              },
              {
                "title": "Sunday",
                "hours": "10am - 7pm",
                "highlight": false
              },
              {
                "title": "half price sale starts",
                "hours": "30 mins prior to close",
                "highlight": true
              }
            ],
            "delivery_options": [
              {
                "location_option": "deliveroo",
                "link_or_phone_number": "https://deliveroo.co.uk/"
              }
            ],
            "distance": 267.06
          },
          {
            "title": "Bishopsgate 155",
            "address_1": "10-11 Broadgate Arcade, 155 Bishopsgate",
            "address_2": "",
            "city": "London",
            "state": "",
            "postal_code": "EC2M 3TQ",
            "country": "UK",
            "telephone": "0207-374-0440",
            "latitude": "51.518902",
            "longitude": "-0.079912",
            "transit_info": "Liverpool Street",
            "wifi_available": true,
            "hours": [{
                "title": "Monday",
                "hours": "9am - 8pm",
                "highlight": false
            }, {
                "title": "Tuesday",
                "hours": "9am - 8pm",
                "highlight": false
            }, {
                "title": "Wednesday",
                "hours": "9am - 8pm",
                "highlight": false
            }, {
                "title": "Thursday",
                "hours": "9am - 8pm",
                "highlight": false
            }, {
                "title": "Friday",
                "hours": "9am - 8pm",
                "highlight": false
            }, {
                "title": "Saturday",
                "hours": "closed",
                "highlight": false
            }, {
                "title": "Sunday",
                "hours": "closed",
                "highlight": false
            }, {
                "title": "half price sale starts",
                "hours": "30 mins prior to close",
                "highlight": true
            }],
            "delivery_options": [],
            "distance": 4.87
        }
          ]}"""

        branches = ItsuApi._parse_branches(json.loads(branch_json))
        lookup_data = LookupGenerator.build_lookup_data(
            branches=branches,
            precision=7
        )
        self.assertEqual(list(lookup_data.time_slot_lookup[40]), [0])
        self.assertEqual(list(lookup_data.time_slot_lookup[88]), [0])
        self.assertEqual(list(lookup_data.time_slot_lookup[136]), [0])
        self.assertEqual(list(lookup_data.time_slot_lookup[184]), [0])
        self.assertEqual(list(lookup_data.time_slot_lookup[232]), [0])
        self.assertEqual(list(lookup_data.time_slot_lookup[280]), [0])
        self.assertEqual(list(lookup_data.time_slot_lookup[325]), [0])
        self.assertEqual(list(lookup_data.time_slot_lookup[39]), [1])
        self.assertEqual(list(lookup_data.time_slot_lookup[87]), [1])
        self.assertEqual(list(lookup_data.time_slot_lookup[135]), [1])
        self.assertEqual(list(lookup_data.time_slot_lookup[183]), [1])
        self.assertEqual(list(lookup_data.time_slot_lookup[231]), [1])

        def combinator(a, b):
            return list(a) + list(b)

        ids = reduce(combinator, lookup_data.time_slot_lookup)
        self.assertEqual(12, len(ids))
        self.assertEqual([1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0], ids)


if __name__ == '__main__':
    unittest.main()
