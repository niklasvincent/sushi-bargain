# sushi-bargain
Find the closest Itsu that will have a half-price sale the soonest.

The geolocation is done entirely in Javascript using HTML5 Geolocation. Since the number of nodes is small (< 100), the time required to calculate the distances and sort by distance and time left is short enough to run on mobile devices.

It also means you do not need any process running on the server, you can simply serve the HTML/CSS/JS/JSON and the browser will perform all the work required.

To generate the `web/sushi-data.json` file required by the web application, simply run:

    python generate.py
    
Afterwards, simply deploy the entirety of `web/` to e.g. Amazon S3.
