from collections import defaultdict

import geohash
import sushi_bargain.restaurant_data_pb2
from google.protobuf.struct_pb2 import ListValue


class LookupGenerator(object):

    @classmethod
    def _build_geohash_lookup(cls, branches, precision):
        """Build geohash lookup table for branches"""
        geo_hash_lookup = defaultdict(list)
        for i, branch in enumerate(branches):
            geo_hash = geohash.encode(
                latitude=branch.position.lat,
                longitude=branch.position.lng,
                precision=precision
            )
            precisions = range(0, precision - 3)
            sub_geo_hashes = [geo_hash[:precision - p] for p in precisions]
            for sub_geo_hash in sub_geo_hashes:
                geo_hash_lookup[sub_geo_hash].append(i)
        return geo_hash_lookup

    @classmethod
    def _time_slot(cls, day_of_the_week, hours):
        """Calculate time slot for given day of the week and hours"""
        if not hours or hours == -1:
            return -1
        return int(day_of_the_week * 24 * 2 + hours * 2)

    @classmethod
    def _times_to_time_slots(cls, half_price_times):
        """Given an array of times, calculate the respective time slots"""
        return [cls._time_slot(i, v) for i, v in enumerate(half_price_times)]

    @classmethod
    def _build_time_slot_lookup(cls, branches):
        """Build time slot lookup array for branches"""
        time_slot_lookup = [ListValue() for _ in range(7 * 24 * 2)]
        for i, branch in enumerate(branches):
            time_slots = cls._times_to_time_slots(
                branch.half_price_times
            )
            for time_slot in time_slots:
                if time_slot > 0:
                    time_slot_lookup[time_slot].extend([i])
        return time_slot_lookup

    @classmethod
    def build_lookup_data(cls, branches, precision):
        """Build complete lookup data for the provided branches"""
        time_slot_lookup = cls._build_time_slot_lookup(
            branches=branches
        )
        geo_hash_lookup = cls._build_geohash_lookup(
            branches=branches,
            precision=precision
        )

        data = sushi_bargain.restaurant_data_pb2.RestaurantData()
        data.shops.extend(branches)
        data.time_slot_lookup.extend(time_slot_lookup)
        data.geo_hash.precision = precision
        for key, values in geo_hash_lookup.items():
            data.geo_hash.lookup[key].extend(values)

        return data
