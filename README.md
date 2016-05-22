# sushi-bargain
Find the closest Itsu that will have a half-price sale the soonest.

The geolocation is done entirely in Javascript using HTML5 Geolocation. Since the number of nodes is small (< 100), the time required to calculate the distances and sort by distance and time left is short enough to run on mobile devices.

It also means you do not need any process running on the server, you can simply serve the HTML/CSS/JS/JSON and the browser will perform all the work required.

## How to run

### Install dependencies

    virtualenv venv
    . ./venv/bin/activate
    pip install -r requirements.txt

### Generate post code lookup table

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

### Generate data file

To generate the `web/sushi-data.json` file required by the web application, simply use `make`:

    make shops

or directly:

    ./bin/sushi-store-lookup-generator.py --postcode-database=postcodes.p --output-directory=./web

It will initially do a big number of HTTP requests, which will be cached for an hour:

    2016-05-22 15:47:24,077 - root - INFO - Trying to deserialise post code lookup table from postcodes.p
    2016-05-22 15:47:48,153 - root - INFO - Wrote final JSON data to ./web/sushi-data.json

### Deploying

Simply deploy the entirety of `web/` to e.g. Amazon S3.
