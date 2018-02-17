import json

import requests
import sushi_bargain.restaurant_data_pb2


class ItsuApi(object):

    days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]

    def __init__(self, base_url=None, latitude=51.530874, longitude=-0.154119):
        if base_url:
            self.base_url = base_url
        else:
            self.base_url = "https://www.itsu.com/locations/search?" \
                    "lat={latitude}&lng={longitude}"
        self.latitude = latitude
        self.longitude = longitude

    @classmethod
    def _time_string_to_float(cls, hours, offset_hours):
        if not hours:
            return None
        hours = hours.replace(" ", "").upper()
        if not hours.endswith("PM"):
            return None
        try:
            t = hours.split("-")[1][:-2].replace(".", ":").split(":")
            hour = float(t[0])
            hour = hour - 12 if hour > 12 else hour
            minute = float(t[1]) if len(t) > 1 else 0
            return 12 + round(hour + minute / 60.0, 2) - offset_hours
        except IndexError:
            return None

    @classmethod
    def _half_price_string_to_offset(cls, hours):
        half_price_keyword = "half price sale starts"

        has_half_price_sale = any(
            [h["title"] == half_price_keyword for h in hours])

        if not has_half_price_sale:
            return None

        # Offset can vary, depending on branch
        # E.g. "30 mins prior to close" or "1 hour prior to close"
        half_price_sale_starts = [h["hours"] for h in hours if
                                  h["title"] == half_price_keyword][0]
        offset = int(
            "".join([c for c in half_price_sale_starts if c.isdigit()]))
        is_in_minutes = "min" in half_price_sale_starts
        offset = offset / 60.0 if is_in_minutes else offset
        return offset

    @classmethod
    def _half_price_hours(cls, hours):
        offset = cls._half_price_string_to_offset(hours)

        if not offset:  # No half price sale offset
            return None

        half_price_hours = {}
        for h in hours:
            if h["title"] in cls.days:
                half_price_hours[h["title"]] = cls._time_string_to_float(
                    h["hours"],
                    offset
                )

        if not any([hour for day, hour in half_price_hours.items()]):
            return None

        half_price_hours_sequence = []
        for day in cls.days:
            half_price_hours_sequence.append(
                half_price_hours.get(day, -1) if half_price_hours.get(
                    day) else -1)

        return half_price_hours_sequence

    @classmethod
    def _parse_branches(cls, data):
        results = []

        for b in data["branches"]:
            half_price_hours = cls._half_price_hours(b["hours"])

            if not half_price_hours:
                continue

            nearest_station = b["transit_info"]
            nearest_station = None if not nearest_station else nearest_station

            shop = sushi_bargain.restaurant_data_pb2.Shop()
            shop.position.lat = float(b["latitude"])
            shop.position.lng = float(b["longitude"])
            shop.name = b["title"]
            shop.post_code = b["postal_code"]

            for value in half_price_hours:
                shop.half_price_times.append(value)

            if nearest_station:
                shop.nearest_station = nearest_station

            results.append(shop)

        return results

    def get_branches(self):
        """Get a list of all branches"""
        search_url = self.base_url.format(
            latitude=self.latitude,
            longitude=self.longitude
        )
        response = requests.get(search_url)

        data = json.loads(
            "{{\"branches\": {}}}".format(response.text)
        )

        return ItsuApi._parse_branches(data)
