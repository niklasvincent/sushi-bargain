#!/usr/bin/env python

import os
import sys
import unittest


from bs4 import BeautifulSoup


sys.path.insert(0, os.path.abspath(os.path.join(*[os.path.realpath(__file__), "..", "..", "sushi-bargain"])))
from itsu import *


test_shop_location_html = """<div id="shoplist-name"><a href="/locations/shops/aldgate_high_street_UK56.html" onmouseout="MM_swapImgRestore()" onmouseover="MM_swapImage('ge_ro_image_PTL9JW3HL0_11','','/graphics/shoplisttitle_/Aldgate+High+Street.gif',0)"><img src="/graphics/shoplisttitle/Aldgate+High+Street.gif" alt="Aldgate High Street" name="ge_ro_image_PTL9JW3HL0_11" border="0" id="ge_ro_image_PTL9JW3HL0_11" /></a></div>
<p id="shoplist-address" style="width: 345px;">77 Aldgate High Street, LONDON,  EC3N 1BD</p>
<div id="shoplist-transport" style="width: 315px;">Aldgate (across the road)</div>
</div>
</div><div id="shoplist-item">
<div id="shoplist-map">
<a onmouseover="MM_swapImage('ge_ro_image_AJL0MJ7AP7_12','','/graphics/clickLocation_button_/click+for+location.gif',0)" onmouseout="MM_swapImgRestore()" href="/locations/shops/baker_street_1_UK36.html"><img border="0" id="ge_ro_image_AJL0MJ7AP7_12" name="ge_ro_image_AJL0MJ7AP7_12" alt="click for location" src="/graphics/clickLocation_button/click+for+location.gif"></a>
<a href="/locations/shops/baker_street_1_UK36.html"><img src="https://maps.google.com/maps/api/staticmap?size=100x80&key=AIzaSyCW5xQg8tKfm9f1u4aKSbMBj6B077gIN3E&amp;center=51.517489,-0.155407&amp;zoom=15&amp;sensor=false&amp;maptype=roadmap&amp;format=png32&amp;markers=color:blue|label:x|icon:http://www.itsu.com/images/map_marker_40.png|51.517489,-0.155407"></a>
</div>
<div id="shoplist-info">
<div id="shoplist-name"><a href="/locations/shops/baker_street_1_UK36.html" onmouseout="MM_swapImgRestore()" onmouseover="MM_swapImage('ge_ro_image_PTL9JW3HL0_12','','/graphics/shoplisttitle_/Baker+Street+1.gif',0)"><img src="/graphics/shoplisttitle/Baker+Street+1.gif" alt="Baker Street 1" name="ge_ro_image_PTL9JW3HL0_12" border="0" id="ge_ro_image_PTL9JW3HL0_12" /></a></div>
<p id="shoplist-address" style="width: 345px;">Unit1, 15 Baker Street, LONDON, W1U 3BX</p>
<div id="shoplist-transport" style="width: 315px;">Bond St (400m)</div>
</div>
</div><div id="shoplist-item">
"""

test_shop_name_html = """<div id="left-content">
<h1 id="pagetitle" ><img  src="/graphics/header/Aldgate.gif" border="0" alt="Aldgate"/></h1>
<div id="shop-image">
<img src="https://itsu.platopusretail.com/assets_scaled/w350/shop_images/m0N6H0U9D220Q134o1P1u4a341C9y.JPG" />
</div>
"""

test_shop_address_html = """<div id="shop-address">
77 Aldgate High Street, LONDON,  EC3N 1BD<br/>
<div id="shop-telephone"><strong>Telephone: </strong>0203 6577038</div>
</div>
"""

test_shop_half_price_times_html = ["""<div id="shop-times">
<h3><img  src="/graphics/shop_subtitle/Opening+Times{COLON}.gif" border="0" alt="Opening+Times:"/></h3>
<table class="opening_times">
<tr><td>Monday</td><td>09:00 - 21:00</td></tr>
<tr><td>Tuesday</td><td>09:00 - 21:00</td></tr>
<tr><td>Wednesday</td><td>09:00 - 21:00</td></tr>
<tr><td>Thursday</td><td>09:00 - 21:00</td></tr>
<tr><td>Friday</td><td>09:00 - 21:00</td></tr>
<tr><td colspan="2" style="color:#E43A94">half-price sale starts at 20:30</td></tr>
<tr><td>Saturday</td><td>Closed</td></tr>
<tr><td>Sunday</td><td>Closed</td></tr>
</table>
</div>
""",
"""<div id="shop-times">
<h3><img  src="/graphics/shop_subtitle/Opening+Times{COLON}.gif" border="0" alt="Opening+Times:"/></h3>
<table class="opening_times">
<tr><td>Monday</td><td>09:00 - 20:00</td></tr>
<tr><td>Tuesday</td><td>09:00 - 20:00</td></tr>
<tr><td>Wednesday</td><td>09:00 - 20:00</td></tr>
<tr><td>Thursday</td><td>09:00 - 20:00</td></tr>
<tr><td>Friday</td><td>09:00 - 20:00</td></tr>
<tr><td colspan="2" style="color:#E43A94">half-price sale starts at 19:30</td></tr>
<tr><td>Saturday</td><td>11:00 - 19:00</td></tr>
<tr><td colspan="2" style="color:#E43A94">half-price sale starts at 18:30</td></tr>
<tr><td>Sunday</td><td>11:00 - 19:00</td></tr>
<tr><td colspan="2" style="color:#E43A94">half-price sale starts at 18:30</td></tr>
</table>
</div>
"""]


class TestItsu(unittest.TestCase):


    def setUp(self):
        self.itsu_website = ItsuWebsite()

    def _str_to_html(self, s):
        return BeautifulSoup(s, "html.parser")


    def test_parse_shop_urls(self):
        html = self._str_to_html(test_shop_location_html)
        self.assertEqual(
            [u'https://www.itsu.com/locations/shops/aldgate_high_street_UK56.html',
             u'https://www.itsu.com/locations/shops/baker_street_1_UK36.html'],
            self.itsu_website._extract_shop_urls(html),
            "Could not parse shop locations correctly"
        )


    def test_time_string_to_float(self):
        self.assertEqual(20.5, self.itsu_website._time_string_to_float("20:30"), "Wrong float time")
        self.assertEqual(8.5, self.itsu_website._time_string_to_float("08:30"), "Wrong float time")
        self.assertEqual(8.5, self.itsu_website._time_string_to_float("8:30"), "Wrong float time")
        self.assertEqual(10.0, self.itsu_website._time_string_to_float("10:00"), "Wrong float")


    def test_extract_shop_name_from_html(self):
        html = self._str_to_html(test_shop_name_html)
        self.assertEqual("Aldgate", self.itsu_website._extract_shop_name_from_html(html), "Wrong shop name extracted")


    def test_extract_shop_address_from_html(self):
        html = self._str_to_html(test_shop_address_html)
        address = self.itsu_website._extract_shop_address_from_html(html)
        self.assertEqual("EC3N1BD", address.post_code(), "Wrong post code extracted")
        self.assertEqual("77 Aldgate High Street, London", address.full(), "Wrong full address extracted")


    def test_extract_shop_half_price_times_from_html(self):
        html = self._str_to_html(test_shop_half_price_times_html[0])
        self.assertEqual(
            [20.5],
            self.itsu_website._extract_shop_half_price_times_from_html(html),
            "Wrong half price time extracted"
        )
        html = self._str_to_html(test_shop_half_price_times_html[1])
        self.assertEqual(
            [19.5, 18.5, 18.5],
            self.itsu_website._extract_shop_half_price_times_from_html(html),
            "Wrong half price time extracted"
        )


if __name__ == '__main__':
    unittest.main()