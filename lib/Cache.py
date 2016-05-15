import hashlib
import logging
import os
import urllib

from StringIO import StringIO
from time import sleep


class Cache(object):

  def __init__(self, cacheDirectory = '../cache'):
    self.cacheDirectory = os.path.join(
      os.path.dirname(os.path.realpath(__file__)),
      cacheDirectory
    )
    # Create cache directory if necessary
    try:
      if not os.path.exists(self.cacheDirectory):
        os.makedirs(self.cacheDirectory)
    except Exception as e:
      logging.error("Could not create cache directory %s: %s", self.cacheDirectory, e)

  def _cacheFilename(self, identifier):
   key = hashlib.md5(str(identifier)).hexdigest()
   cacheFileName = os.path.join(self.cacheDirectory, key)
   return cacheFileName

  def __getitem__(self, identifier):
    cacheFileName = self._cacheFilename(identifier)
    logging.debug("Cache filename is %s", cacheFileName)
    if os.path.exists(cacheFileName):
      logging.debug("Cache hit at %s", cacheFileName)
      return open(cacheFileName, 'r')
    else:
      if not identifier.startswith('http'):
        logging.warn("Not in cache and not a URL: %s", identifier)
        return None
      url = identifier
      logging.debug("Will download %s in 1 second", url)
      sleep(1)
      try:
          f = urllib.urlopen(url)
          content = f.read()
          with open(cacheFileName, 'w') as c:
            c.write(content)
          data = StringIO()
          data.write(content)
      except Exception as e:
          logging.error("Could not download %s: %s", url, e)
          data = None
    return data


  def __setitem__(self, identifier, data):
    cacheFileName = self._cacheFilename(identifier)
    with open(cacheFileName, 'w') as c:
      c.write(data)
