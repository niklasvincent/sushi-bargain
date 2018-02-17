[![Build Status](https://travis-ci.org/nlindblad/sushi-bargain.svg?branch=master)](https://travis-ci.org/nlindblad/sushi-bargain)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](http://opensource.org/licenses/MIT)
# sushi-bargain
**Problem**: Find the closest Itsu that will have a half-price sale the soonest.

Generates a JSON data file than can be used by [sushi-bargain-frontend](https://github.com/nlindblad/sushi-bargain-frontend).

## How to run

### Install dependencies

    make install

### Generate data file

    sushi-bargain --output-directory OUTPUT_DIRECTORY

## Development

The unit tests are residing in `tests` and can be run via:

    tox