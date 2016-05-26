#!/usr/bin/env python

import argparse
import json
import os
import sys
from collections import defaultdict


import geohash

sys.path.insert(0, os.path.abspath(os.path.join(*[os.path.realpath(__file__), "..", "..", "sushi-bargain"])))
from time_slot import *


def serialise_optimised_data(itsu_branches, time_slot_lookup, geo_hash_lookup, precision):
    """Serialise optimised branch data to JSON"""
    return json.dumps({
        "geo_hash": {
            "precision": precision,
            "lookup": geo_hash_lookup
        },
        "time_slot_lookup": time_slot_lookup,
        "shops": itsu_branches
    })


def build_geohash_lookup(itsu_branches, precision):
    """Build geohash lookup table for branches"""
    geo_hash_lookup = defaultdict(list)
    for i, itsu_branch in enumerate(itsu_branches):
        geo_hash = geohash.encode(
            latitude=itsu_branch["position"]["lat"],
            longitude=itsu_branch["position"]["lng"],
            precision=precision
        )
        for sub_geo_hash in [geo_hash[:precision-j] for j in xrange(0, precision - 3)]:
            geo_hash_lookup[sub_geo_hash].append(i)
    return geo_hash_lookup


def build_time_slot_lookup(itsu_branches):
    """Build time slot lookup array for branches"""
    time_slot_lookup = empty_time_slot_lookup_array()
    for i, itsu_branch in enumerate(itsu_branches):
        for time_slot in times_to_time_slots(itsu_branch["half_price_times"]):
            if time_slot > 0:
                time_slot_lookup[time_slot].append(i)
    return time_slot_lookup


def setup_logging(debug=False):
    """Set up logging"""
    from logger import getLogger
    global logging
    logging = getLogger()


def parse_args():
    """Parse command line arguments"""
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument(
        "--debug",
        help="Increase output verbosity",
        action="store_true")
    args_parser.add_argument(
        "--input-directory",
        required=True,
        help="Input directory")
    args_parser.add_argument(
        "--output-directory",
        required=True,
        help="Output directory")
    args = args_parser.parse_args()
    return args


def main(input_filename, output_filename, precision):
    args = parse_args()
    setup_logging(args.debug)

    input_filename_full = os.path.join(args.input_directory, input_filename)
    output_filename_full = os.path.join(args.output_directory, output_filename)

    try:
        with open(input_filename_full, 'r') as f:
            itsu_branches = json.load(f)
        logging.info("Deserialised input %s", input_filename)
    except Exception as e:
        logging.error("Error deserialising input %s: %s", input_filename, e)
        sys.exit(1)

    time_slot_lookup = build_time_slot_lookup(itsu_branches=itsu_branches)
    geo_hash_lookup  = build_geohash_lookup(itsu_branches=itsu_branches, precision=precision)

    try:
        with open(output_filename_full, 'w') as f:
            f.write(serialise_optimised_data(
                itsu_branches=itsu_branches,
                time_slot_lookup=time_slot_lookup,
                geo_hash_lookup=geo_hash_lookup,
                precision=precision
            ))
        logging.info("Serialised optimised data to output %s", output_filename)
    except Exception as e:
        logging.error("Error optimised data to output %s: %s", output_filename, e)


if __name__ == "__main__":
    main(
        input_filename="sushi-data.json",
        output_filename="sushi-data-optimised.json",
        precision=7
    )
