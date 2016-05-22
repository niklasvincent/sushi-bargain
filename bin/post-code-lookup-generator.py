#!/usr/bin/env python

import argparse
import zipfile
import os
import sys
from StringIO import StringIO

try:
   import cPickle as pickle
except:
   import pickle


sys.path.insert(0, os.path.abspath(os.path.join(*[os.path.realpath(__file__), "..", "..", "sushi-bargain"])))
from postcode import *


import requests
from clint.textui import progress


def download_database(url):
    """Download database and store in-memory"""
    logging.info("Starting download of %s", url)
    try:
        filename = url.split('/')[-1]
        r = requests.get(url, stream=True)
        data = StringIO()
        total_length = int(r.headers.get('content-length'))
        for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1):
            if chunk:
                data.write(chunk)
        return filename, data
    except Exception as e:
        logging.error("Could not download %s: %s", url, e)
        sys.exit(1)


def unpack_database(filename, data):
    """Unpack database in-memory"""
    csv_filename = filename.replace('.zip', '.csv')
    logging.info("Attempting to decompress %s from within %s", csv_filename, filename)
    try:
        zip_data = zipfile.ZipFile(data)
        with zip_data.open(csv_filename) as csv_data:
            return csv_data.readlines()
    except Exception as e:
        logging.error("Could not decompress %s: %s", csv_filename, e)
        sys.exit(2)


def serialise_lookup_table(table):
    """Serialise lookup table"""
    return pickle.dumps(table)


def serialise_lookup_table_to_disk(filename, table):
    """Serialise lookup table to disk"""
    try:
        with open(filename, 'wb') as f:
            f.write(serialise_lookup_table(table))
        logging.info("Wrote serialied lookup table to %s", filename)
    except Exception as e:
        logging.error("Could not write serialised lookup table to %s: %s", filename, e)
        sys.exit(3)


def setup_logging(debug=False):
    """Set up logging"""
    from logger import getLogger
    global logging
    logging = getLogger(debug)


def parse_args():
    """Parse command line arguments"""
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument(
        "--debug",
        help="Increase output verbosity",
        action="store_true")
    args_parser.add_argument(
        "--database-url",
        required=True,
        help="UK post code database URL")
    args_parser.add_argument(
        "--output-directory",
        required=True,
        help="Output directory")
    args = args_parser.parse_args()
    return args


def main(output_filename):
    args = parse_args()
    setup_logging(args.debug)
    filename, data = download_database(url=args.database_url)
    csv_data = unpack_database(filename=filename, data=data)
    table = construct_lookup_table(csv_data=csv_data)

    # Output filename
    output_filename_full = os.path.join(args.output_directory, output_filename)
    serialise_lookup_table_to_disk(filename=output_filename_full, table=table)


if __name__ == "__main__":
    main(output_filename="postcodes.p")