#!/usr/bin/env python

import json
import unittest

from sushi_bargain.itsu import ItsuApi


class TestItsu(unittest.TestCase):
    def test_parse_time(self):
        self.assertEqual(
            20.0,
            ItsuApi._time_string_to_float("10am - 8.30pm", 0.5)
        )
        self.assertEqual(
            18.5,
            ItsuApi._time_string_to_float("10am - 7pm", 0.5)
        )
        self.assertEqual(
            18.0,
            ItsuApi._time_string_to_float("10am - 7pm", 1.0)
        )
        self.assertEqual(
            17.0,
            ItsuApi._time_string_to_float("10am - 17.30pm", 0.5)
        )

    def test_half_price_string_to_offset_30_mins(self):
        self.assertEqual(
            0.5,
            ItsuApi._half_price_string_to_offset(
                [{
                    "title": "half price sale starts",
                    "hours": "30 mins prior to close",
                    "highlight": True
                }]
            )
        )

    def test_half_price_string_to_offset_1_hours(self):
        self.assertEqual(
            1.0,
            ItsuApi._half_price_string_to_offset(
                [{
                    "title": "half price sale starts",
                    "hours": "1 hour prior to close",
                    "highlight": True
                }]
            )
        )

    def test_half_price_string_to_offset_no_offset(self):
        self.assertIsNone(
            ItsuApi._half_price_string_to_offset(
                [{
                    "title": "Monday",
                    "hours": "10am - 8.30pm",
                    "highlight": False
                }]
            )
        )

    def test_half_price_hours(self):
        hours = [
              {
                "title": "Monday",
                "hours": "10am - 8.30pm",
                "highlight": False
              },
              {
                "title": "Tuesday",
                "hours": "10am - 8.30pm",
                "highlight": False
              },
              {
                "title": "Wednesday",
                "hours": "10am - 8.30pm",
                "highlight": False
              },
              {
                "title": "Thursday",
                "hours": "10am - 8.30pm",
                "highlight": False
              },
              {
                "title": "Friday",
                "hours": "10am - 8.30pm",
                "highlight": False
              },
              {
                "title": "Saturday",
                "hours": "10am - 8.30pm",
                "highlight": False
              },
              {
                "title": "Sunday",
                "hours": "10am - 7pm",
                "highlight": False
              },
              {
                "title": "half price sale starts",
                "hours": "30 mins prior to close",
                "highlight": True
              }
            ]
        half_price_hours = ItsuApi._half_price_hours(hours)
        self.assertEquals(
            [20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 18.5],
            half_price_hours
        )

    def test_parse_branch(self):
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
          }]}"""

        branches = ItsuApi._parse_branches(json.loads(branch_json))
        self.assertEqual(1, len(branches))
        self.assertEqual("Leeds Commercial Street", branches[0].name)
        self.assertAlmostEqual(53.79725, branches[0].position.lat, places=4)
        self.assertAlmostEqual(-1.54450, branches[0].position.lng, places=4)
        self.assertEqual(20.0, branches[0].half_price_times[0])
        self.assertEqual(20.0, branches[0].half_price_times[1])
        self.assertEqual(20.0, branches[0].half_price_times[2])
        self.assertEqual(20.0, branches[0].half_price_times[3])
        self.assertEqual(20.0, branches[0].half_price_times[4])
        self.assertEqual(20.0, branches[0].half_price_times[5])
        self.assertEqual(18.5, branches[0].half_price_times[6])

    def test_parse_branch_24_hour_time(self):
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
                "hours": "11am - 17.30pm",
                "highlight": false
              },
              {
                "title": "Tuesday",
                "hours": "11am - 17.30pm",
                "highlight": false
              },
              {
                "title": "Wednesday",
                "hours": "11am - 17.30pm",
                "highlight": false
              },
              {
                "title": "Thursday",
                "hours": "11am - 17.30pm",
                "highlight": false
              },
              {
                "title": "Friday",
                "hours": "11am - 17.30pm",
                "highlight": false
              },
              {
                "title": "Saturday",
                "hours": "closed",
                "highlight": false
              },
              {
                "title": "Sunday",
                "hours": "closed",
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
          }]}"""

        branches = ItsuApi._parse_branches(json.loads(branch_json))
        self.assertEqual(1, len(branches))
        self.assertEqual(17.0, branches[0].half_price_times[0])
        self.assertEqual(17.0, branches[0].half_price_times[1])
        self.assertEqual(17.0, branches[0].half_price_times[2])
        self.assertEqual(17.0, branches[0].half_price_times[3])
        self.assertEqual(17.0, branches[0].half_price_times[4])
        self.assertEqual(-1.0, branches[0].half_price_times[5])
        self.assertEqual(-1.0, branches[0].half_price_times[6])

    def test_parse_branch_with_weird_hours(self):
        branch_json = """{"branches": [{
            "title": "Islington Angel Central",
            "postal_code": "N1 0PS",
            "latitude": "51.534325",
            "longitude": "-0.106258",
            "transit_info": "Angel",
            "hours": [{
                "title": "Monday",
                "hours": "04:30am - 30 minutes before the last flight",
                "highlight": false
            }, {
                "title": "Tuesday",
                "hours": "04:30am - 30 minutes before the last flight",
                "highlight": false
            }, {
                "title": "Wednesday",
                "hours": "04:30am - 30 minutes before the last flight",
                "highlight": false
            }, {
                "title": "Thursday",
                "hours": "04:30am - 30 minutes before the last flight",
                "highlight": false
            }, {
                "title": "Friday",
                "hours": "04:30am - 30 minutes before the last flight",
                "highlight": false
            }, {
                "title": "Saturday",
                "hours": "04:30am - 30 minutes before the last flight",
                "highlight": false
            }, {
                "title": "Sunday",
                "hours": "04:30am - 30 minutes before the last flight",
                "highlight": false
            }, {
                "title": "half price sale starts",
                "hours": "30 mins prior to close",
                "highlight": true
            }]
        }]}"""

        branches = ItsuApi._parse_branches(json.loads(branch_json))
        self.assertEqual(0, len(branches))


if __name__ == '__main__':
    unittest.main()
