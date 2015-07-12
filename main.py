import hashlib
import os
import urllib



from bs4 import BeautifulSoup

CACHE_DIR = 'cache'

ITSU_BASE_DOMAIN = "https://www.itsu.com"

buildUrl = lambda x: ITSU_BASE_DOMAIN + x

ITSU_LOCATIONS_URL = buildUrl("/locations/shops/")

def parse(url):
  cacheFileName = os.path.join(CACHE_DIR, hashlib.md5(url).hexdigest())
  if os.path.exists(cacheFileName):
    f = open(cacheFileName, 'r')
    html = f.read()
  else:
    f = urllib.urlopen(url)
    html = f.read()
    cachedFile = open(cacheFileName, 'w')
    cachedFile.write(html)
  soup = BeautifulSoup(html, "html.parser")
  return soup

def getAllShopUrls():
  return [buildUrl(link['href']) for link in parse(ITSU_LOCATIONS_URL).select("#shoplist-name a")]

def getHalfPriceTimes(shopUrl):
  nearestStation = parse(shopUrl).select('#shop-address')[0].text
  halfPriceTimes = [td.text for td in parse(shopUrl).select('#shop-times td') if 'half-price' in td.text]
  return (nearestStation, halfPriceTimes)

def main():
  for shopUrl in getAllShopUrls():
    halfPriceTimes = getHalfPriceTimes(shopUrl)
    if halfPriceTimes[1]:
      print "\n%s" % halfPriceTimes[0], "\n=================="
      print "Weekdays: %s" % halfPriceTimes[1][0]
      if len(halfPriceTimes[1]) > 1:
        print "Saturdays: %s" % halfPriceTimes[1][1]
      if len(halfPriceTimes[1]) > 2:
        print "Sundays: %s" % halfPriceTimes[1][1]



if __name__ == "__main__":
  main()