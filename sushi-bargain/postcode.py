from model import *

def process_line(csv_line):
    """Process single line from post code database CSV"""
    line = csv_line.strip().split(',')
    if len(line) != 4:
        return None
    post_code = line[1].replace(' ', '')
    latitude = float(line[2])
    longitude = float(line[3])
    return PostCode(post_code=post_code, position=Position(latitude=latitude, longitude=longitude))


def construct_lookup_table(csv_data):
    """Construct lookup table between post code and coordinates"""
    table = {}
    # Skip header row
    for csv_line in csv_data[1:]:
        post_code = process_line(csv_line)
        if post_code:
            table[post_code.post_code] = post_code.position
    return table
