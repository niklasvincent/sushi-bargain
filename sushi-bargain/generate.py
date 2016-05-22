import json
import logging
import sys

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
  itsuBranches = itsu.get_half_price_times()

  outputFilename = config["output_filename"]
  logging.debug("Writing generated data to %s", outputFilename)
  with open(outputFilename, 'w') as f:
    f.write(json.dumps(constructGeographicalData(itsuBranches, geoLocator)))


if __name__ == "__main__":
  main(configFile = "config.json")
