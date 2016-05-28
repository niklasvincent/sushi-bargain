[![Build Status](https://travis-ci.org/nlindblad/sushi-bargain.svg?branch=master)](https://travis-ci.org/nlindblad/sushi-bargain)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](http://opensource.org/licenses/MIT)
# sushi-bargain
**Problem**: Find the closest Itsu that will have a half-price sale the soonest.

Generates a JSON data file than can be used by [https://github.com/nlindblad/sushi-bargain-frontend](sushi-bargain-frontend).

## Structure

There are three components:

### `post-code-lookup-generator.py`

1. Download a compressed CSV file of UK postcodes and their corresponding latitude/longitude
2. Unpack the compressed CSV
3. Constructs a lookup table and serialises it using Python's pickle object serialisation

### `sushi-store-lookup-generator.py`

1. Scrapes the URLs of each individual branch
2. Extracts key information (name, address, opening hours) from the individual page of each branch
3. Deserialises the UK postcodes lookup table and supplements the information about each branch with its longitude/latitude

### `sushi-store-optimised-generator.py`

1. Generate a time slot lookup table for sales times
2. Generate a [GeoHash](https://en.wikipedia.org/wiki/Geohash) lookup table for stores

## How to run

### Install dependencies

    make install

### Generate data file

    make all

### Generate data files in steps

#### Generate post code lookup table

Either through `make`:

    make postcodes

or directly:

     ./bin/post-code-lookup-generator.py --database-url https://www.freemaptools.com/download/full-postcodes/ukpostcodes.zip --output-directory .

It will take a couple of minutes to download and build the lookup table for post codes to coordinates:

    2016-05-22 13:36:44,193 - root - INFO - Starting download of https://www.freemaptools.com/download/full-postcodes/ukpostcodes.zip
    2016-05-22 13:36:44,205 - requests.packages.urllib3.connectionpool - INFO - Starting new HTTPS connection (1): www.freemaptools.com
    [################################] 33458/33458 - 00:01:06
    2016-05-22 13:37:51,648 - root - INFO - Attempting to decompress ukpostcodes.csv from within ukpostcodes.zip
    2016-05-22 13:38:09,501 - root - INFO - Wrote serialied lookup table to ./postcodes.p

#### Generate data file

To generate the `web/sushi-data.json` file, simply use `make`:

    make shops

or directly:

    ./bin/sushi-store-lookup-generator.py --postcode-database=postcodes.p --output-directory=./web

It will initially do a big number of HTTP requests, which will be cached for an hour:

    2016-05-22 15:47:24,077 - root - INFO - Trying to deserialise post code lookup table from postcodes.p
    2016-05-22 15:47:48,153 - root - INFO - Wrote final JSON data to ./web/sushi-data.json


#### Generate optimised data file

To generate the `web/sushi-data-optimised.json` file required by the [https://github.com/nlindblad/sushi-bargain-frontend](web application), simply use `make`:

    make optimise

or directly:

    ./bin/sushi-store-optimised-generator.py --input-directory=./web --output-directory=./web

It will do a quick augmentation of the data:

    2016-05-28 15:56:48,225 - root - INFO - Deserialised input sushi-data.json
    2016-05-28 15:56:48,226 - root - INFO - Serialised optimised data to output sushi-data-optimised.json

## Development

The unit tests are residing in `tests` and can be run via:

    make test