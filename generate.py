import json
import logging
import os
import re
import sys
import traceback
import zipfile

from collections import namedtuple
from StringIO import StringIO

from bs4 import BeautifulSoup

from lib.Cache import Cache


class Address(object):


  def __init__(self, address):
    self.postCodeRegexp = re.compile(r"\b[A-Z]{1,2}[0-9][A-Z0-9]?\s?[0-9][ABD-HJLNP-UW-Z]{2}\b")
    try:
      self.address = str(str(address).strip().split('\n')[0])
    except Exception as e:
      logging.error("Could not format address: %s", address)


  def postCode(self):
    """Get the post code"""
    try:
      return re.findall(self.postCodeRegexp, self.address)[0].replace(' ', '')
    except Exception as e:
      logging.error("Could not extract post code from address: %s", self.address)

  def full(self):
    """Get the full address"""
    try:
      return ", ".join(self.address.split(', ')[0:-1]).lower().title()
    except Exception as e:
      logging.error("Could not format full address: %s", self.address)


class GeoLocator(object):


  def __init__(self, databaseUrl):
    self.databaseUrl = databaseUrl
    self.cache = Cache()
    data = self._constructDatabase(self.databaseUrl)
    self.database = json.load(data)

  def __constructLookUpTable(self, data):
    """Construct a look up table between post codes and coordinates"""
    table = {}
    for line in data[1:]:
      try:
        l = [i.strip() for i in line.split(',')]
        table[l[1].replace(' ', '')] = (float(l[2]), float(l[3]))
      except Exception as e:
        logging.error("Could not construct look up record for line: %s", line)
    return table


  def _constructDatabase(self, url):
    """Fetch database file from URL and construct look up table"""
    cacheKey = "post_code_lookup_db"
    data = self.cache["post_code_lookup_db"]
    if not data:
      logging.debug("Fetching postcode to coordinate database from URL %s", url)
      filename = url.split('/')[-1].replace('.zip', '.csv')
      compressedArchive = zipfile.ZipFile(self.cache[url])
      databaseFile = compressedArchive.open(filename)
      content = json.dumps(self.__constructLookUpTable(databaseFile.readlines()))
      self.cache["post_code_lookup_db"] = content
      data = StringIO()
      data.write(content)
    return data


  def coordinatesForPostCode(self, postCode):
    """Get coordinates for a UK post code"""
    coordinates = self.database.get(postCode, (0.0, 0.0))
    return coordinates


ItsuBranch = namedtuple("ItsuBranch", ["name", "address", "postCode", "weekday", "saturday", "sunday"])


class ItsuWebsite(object):

  def __init__(self, baseDomain = "https://www.itsu.com"):
    self.baseDomain = baseDomain
    self.timeRegexp = re.compile(r"[0-9]{1,2}:[0-9]{1,2}")
    self.cache = Cache()


  def _buildUrl(self, relativeUrl):
    return self.baseDomain + relativeUrl


  def _fetchHTML(self, url):
    """Fetch HTML from URL"""
    logging.debug("Fetching HTML for URL %s", url)
    html = self.cache[url].read()
    return html


  def _parseHTML(self, url):
    """Return HTML from URL parsed with BeautifulSoup"""
    logging.debug("Parsing HTML for URL %s", url)
    html = self._fetchHTML(url)
    soup = BeautifulSoup(html, "html.parser")
    return soup


  def _getAllShopUrls(self):
    """Get the URL of all Itsu shops"""
    logging.debug("Getting list of all Itsu shops")
    locationsUrl = self._buildUrl("/locations/shops/")
    shopUrls = [self._buildUrl(link['href']) for link in self._parseHTML(locationsUrl).select("#shoplist-name a")]
    return shopUrls


  def _getHalfPriceTimesForShop(self, shopUrl):
    """Get the half price time and post code for a given Itsu shop URL"""
    def getItem(l, i, default = None):
      try:
        return l[i]
      except IndexError:
        return default

    def timeStringToFloat(time):
      t = time.split(':')
      return round(float(t[0]) + float(t[1])/60.0, 2)

    html = self._parseHTML(shopUrl)
    name = html.select('#pagetitle img')[0].get('alt', 'Unknown branch name')
    address = Address(html.select('#shop-address')[0].text)
    halfPriceTimes = [timeStringToFloat(self.timeRegexp.findall(td.text)[0]) for td in html.select('#shop-times td') if 'half-price' in td.text]

    itsuBranch = ItsuBranch(
      name,
      address.full(),
      address.postCode(),
      getItem(halfPriceTimes, 0),
      getItem(halfPriceTimes, 1),
      getItem(halfPriceTimes, 2)
    )
    return itsuBranch


  def getHalfPriceTimes(self):
    """Get a list of all Itsue half price times"""
    results = []
    for shopUrl in self._getAllShopUrls():
      try:
        halfPriceTimes = self._getHalfPriceTimesForShop(shopUrl)
        results.append(halfPriceTimes)
      except Exception as e:
        logging.error("Exception when processing %s: %s", shopUrl, e)
        logging.debug(traceback.format_exc())
        continue
    return results

def constructGeographicalData(itsuBranches, geoLocator):
  geographicalData = []
  for itsuBranch in itsuBranches:
    latitude, longitude = geoLocator.coordinatesForPostCode(itsuBranch.postCode)
    if itsuBranch.weekday or itsuBranch.saturday or itsuBranch.sunday:
      geographicalData.append(
        {
          "position" : {"lat" : latitude, "lng": longitude},
          "name" : itsuBranch.name,
          "postCode" : itsuBranch.postCode,
          "address" : itsuBranch.address,
          "halfPriceTimes" : [itsuBranch.sunday] + 5 * [itsuBranch.weekday] + [itsuBranch.saturday]
        }
      )
  return geographicalData

def main(configFile):
  # Parse config file
  try:
    with open(configFile) as f:
      config = json.load(f)
  except Exception as e:
    logger.error("Could not load configuration file %s: %s", configFile, e)
  # Set up logging
  root = logging.getLogger()
  ch = logging.StreamHandler(sys.stdout)
  formatter = logging.Formatter(
      '%(asctime)s - sushi-bargain - %(levelname)s - %(message)s')
  ch.setFormatter(formatter)
  root.addHandler(ch)
  ch.setLevel(logging.DEBUG)
  root.setLevel(logging.DEBUG)

  geoLocator = GeoLocator(config["post_code_db_url"])

  itsu = ItsuWebsite()
  itsuBranches = itsu.getHalfPriceTimes()

  outputFilename = config["output_filename"]
  logging.debug("Writing generated data to %s", outputFilename)
  with open(outputFilename, 'w') as f:
    f.write(json.dumps(constructGeographicalData(itsuBranches, geoLocator)))


if __name__ == "__main__":
  main(configFile = "config.json")
