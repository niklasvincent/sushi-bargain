#!/usr/bin/env python

import argparse
import json
import os
import sys


try:
   import cPickle as pickle
except:
   import pickle


import requests_cache


sys.path.insert(0, os.path.abspath(os.path.join(*[os.path.realpath(__file__), "..", "..", "sushi-bargain"])))
from address import *
from itsu import *


def populate_positions_for_branches(post_code_lookup_table, itsu_branches):
    """Populates the latitude/longitude of each branch using the provided lookup table"""
    itsu_branches_with_position = []
    for i, itsu_branch in enumerate(itsu_branches):
        itsu_branches_with_position.append(itsu_branch._replace(position=post_code_lookup_table.get(itsu_branch.post_code)))
    return itsu_branches_with_position

def deserialise_post_code_lookup_table(postcode_database_filename):
    """Deserialise a previously deserialised post code lookup table"""
    logging.info("Trying to deserialise post code lookup table from %s", postcode_database_filename)
    try:
        with open(postcode_database_filename, 'rb') as f:
            return pickle.load(f)
    except Exception as e:
        logging.error("Could not deserialise post code lookup table from %s: %s", postcode_database_filename, e)
        sys.exit(2)


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
        "--postcode-database",
        required=True,
        help="UK post code database filename")
    args_parser.add_argument(
        "--output-directory",
        required=True,
        help="Output directory")
    args = args_parser.parse_args()
    return args


def main(output_filename):
    args = parse_args()
    setup_logging(args.debug)

    output_filename_full = os.path.join(args.output_directory, output_filename)

    # Make sure requests get cached
    requests_cache.install_cache('web_cache', backend='sqlite', expire_after=3600)

    post_code_table = deserialise_post_code_lookup_table(postcode_database_filename=args.postcode_database)

    itsu_website = ItsuWebsite()

    itsu_branches = populate_positions_for_branches(
        post_code_lookup_table=post_code_table,
        itsu_branches=itsu_website.get_itsu_branches()
    )

    try:
        with open(output_filename_full, 'w') as f:
            json.dump(itsu_branches, f)
        logging.info("Wrote final JSON data to %s", output_filename_full)
    except Exception as e:
        logging.info("Could not write final JSON data to %s: %s", output_filename_full, e)




if __name__ == "__main__":
    main(output_filename="sushi-data.json")
