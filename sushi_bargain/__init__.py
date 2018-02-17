#!/usr/bin/env python

import argparse
import logging
import os
import sys

from google.protobuf.json_format import MessageToJson
from sushi_bargain.itsu import ItsuApi
from sushi_bargain.lookup import LookupGenerator


def setup_logging(debug=False):
    """Set up logging"""
    root = logging.getLogger()
    ch = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)
    if debug:
        ch.setLevel(logging.DEBUG)
        root.setLevel(logging.DEBUG)
    else:
        ch.setLevel(logging.INFO)
        root.setLevel(logging.INFO)


def parse_args():
    """Parse command line arguments"""
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument(
        "--debug",
        help="Increase output verbosity",
        action="store_true")
    args_parser.add_argument(
        "--output-directory",
        required=True,
        help="Output directory")
    args = args_parser.parse_args()
    return args


def main(output_filename="sushi-data-optimised.json", precision=7):
    args = parse_args()
    setup_logging(args.debug)

    output_filename_full = os.path.join(args.output_directory, output_filename)

    itsu_website = ItsuApi()

    itsu_branches = itsu_website.get_branches()
    data = LookupGenerator.build_lookup_data(
        branches=itsu_branches,
        precision=precision
    )
    json_data = MessageToJson(data)
    with open(output_filename_full, "w") as f:
        f.write(json_data)
