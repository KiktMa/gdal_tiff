#!/usr/bin/env python 
# coding:utf-8
import sys
import traceback
import json
import argparse
from octant_to_latlong import LatLonBox
from find_overlaps import find_overlaps
import copy

def restricted_float(x):
    try:
        x = float(x)
    except ValueError:
        raise argparse.ArgumentTypeError("%r not a floating-point literal" % (x,))

    if x < -180.0 or x > 180.0:
        raise argparse.ArgumentTypeError("%r not in range [-180.0, +180.0]"%(x,))
    return x

def parse_args():
    description = "usage: % prog[options]"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-s', '--south', type=restricted_float, required=True, help='The latitudes of left bottom point')
    parser.add_argument('-w', '--west', type=restricted_float, required=True, help='The longitude of left bottom point')
    parser.add_argument('-n', '--north', type=restricted_float, required=True, help='The latitudes of right top point')
    parser.add_argument('-e', '--east', type=restricted_float, required=True, help='The longitude of right top point')
    parser.add_argument('-g', '--grid', required=True, help='The grid config file for map of selected area')
 
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()
    filename = args.grid
    bottom = args.south
    top = args.north
    bottom, top = sorted([bottom, top])
    left = args.west
    right = args.east
    left, right = sorted([left, right])
    volume = [bottom, left, top, right]
    bbox = LatLonBox(north=top, south=bottom, west=left, east=right)
    print(bbox)
    octants = find_overlaps(bbox, max_octants_per_level=10)
    
    grid_dict = {
        'version': "1.0",
        'volume': volume,
        'grids': octants,
    }

    json_str = json.dumps(grid_dict, default=lambda o: o.__dict__, sort_keys=True)
    with open(filename, 'w') as json_file:
        json_file.write(json_str)
