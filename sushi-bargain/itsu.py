import re

import requests
from bs4 import BeautifulSoup


from address import *
from model import *


class ItsuWebsite(object):


  def __init__(self, base_domain ="https://www.itsu.com"):
    self.base_domain = base_domain
    self.time_regexp = re.compile(r"[0-9]{1,2}:[0-9]{1,2}")


  def _time_string_to_float(self, time):
      t = time.split(':')
      return round(float(t[0]) + float(t[1]) / 60.0, 2)


  def _buildUrl(self, relative_url):
    return self.base_domain + relative_url


  def _fetch_html(self, url):
    """Fetch HTML from URL"""
    r = requests.get(url)
    return r.text


  def _parse_html(self, url):
    """Return HTML from URL parsed with BeautifulSoup"""
    html = self._fetch_html(url)
    soup = BeautifulSoup(html, "html.parser")
    return soup


  def _extract_shop_urls(self, html):
    """Extract the URL of all Itsu shops from provided HTML"""
    return [self._buildUrl(link['href']) for link in html.select("#shoplist-name a")]


  def _get_all_shop_urls(self):
    """Get the URL of all Itsu shops"""
    return self._extract_shop_urls(self._parse_html(self._buildUrl("/locations/shops/")))


  def _extract_shop_half_price_times_from_html(self, html):
    """Get the half price time for shop from HTML"""
    return [self._time_string_to_float(self.time_regexp.findall(td.text)[0]) for td in html.select('#shop-times td') if 'half-price' in td.text]


  def _extract_shop_address_from_html(self, html):
      """Get the shop address from HTML"""
      return Address(html.select('#shop-address')[0].text)


  def _extract_shop_name_from_html(self, html):
      """Get the shop name from HTML"""
      return html.select('#pagetitle img')[0].get('alt', 'Unknown branch name')


  def _extract_itsu_branch_details_from_html(self, html):
    def get_item(l, i, default = None):
      try:
        return l[i]
      except IndexError:
        return default

    name = self._extract_shop_name_from_html(html)
    address = self._extract_shop_address_from_html(html)
    half_price_times = self._extract_shop_half_price_times_from_html(html)

    itsu_branch = ItsuBranch(
      name=name,
      address=address.full(),
      post_code=address.post_code(),
      weekday=get_item(half_price_times, 0),
      saturday=get_item(half_price_times, 1),
      sunday=get_item(half_price_times, 2),
      position=None
    )
    return itsu_branch


  def get_itsu_branches(self):
    """Get a list of all Itsu branches """
    from logger import getLogger
    global logging
    logging = getLogger()
    results = []
    for shop_url in self._get_all_shop_urls():
      try:
        html =  self._parse_html(shop_url)
        itsu_branch = self._extract_itsu_branch_details_from_html(html)
        results.append(itsu_branch)
      except Exception as e:
        logging.warn("Error processing branch: %s", e)
        continue
    return results