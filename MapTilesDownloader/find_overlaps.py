import sys
import time
import traceback
import codecs
import requests
from google.protobuf.message import DecodeError
from collections import defaultdict, OrderedDict
import json
from urllib.request import urlopen, URLError
from urllib.parse import urlencode
from proto.rocktree_pb2 import BulkMetadata
from proto.rocktree_pb2 import PlanetoidMetadata
import loger
from octant_to_latlong import octant_to_latlong
from octant_to_latlong import LatLonBox

PLANET = "earth"
URL_PREFIX = f"https://kh.google.com/rt/{PLANET}/"

# Headers for URL GET requests, can be used in the future to fool google servers:
headers = {
    'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:42.0) Gecko/20100101 Firefox/42.0'      # may be used later to fool server
}

def requestData(url, query, headers=None, msgHint=''):
    """
    Sends GET URL request formed from a base url, a query string
    and headers. Returns whatever this request receives back.
    :param url: string - base URL
    :param query: dictionary - url query paramteres as key-value
    :param headers: dictionary - header parameters as key-value
    :return: dictionary - data from returned JSON
    """
    # URL GET request
    query_str = urlencode(query).encode('ascii') if len(query) else ''
    decoded_query_str = f'?{query_str.decode()}' if len(query_str) else ''
    # Repeat HTTP request if failure (e.g. unstable internet connection)
    response = None

    max_trials = 10
    trials_remain = max_trials                  # max trials
    while not response:
        trials_remain -= 1
        try:
            response = requests.get(url + decoded_query_str, headers=headers)
            response.raise_for_status() # raises if 4xx or 5xx error code
            if response.status_code == 101:
                raise DecodeError
        except DecodeError:
            loger.error('%sStatus code %d: This panorama is recently being updated. Please, try later.'\
                            % (msgHint, 101)
                        )
            return None
        except Exception:
            if trials_remain == 0:
                loger.warning(msgHint + 'Max trials of the URL request reached.\n' \
                                + response.url + '\nStatus code: ' + response.status_code)
                loger.exception()
                return None

    return response

def urlread(url):
    for i in range(50):
        try:
            handle = urlopen(url)
            return  handle.read()
        except URLError:
            # typ, val, tb = sys.exc_info()
            # print(traceback.format_exception(typ, val, tb))
            if i == 49:
                raise Exception("Max retries exceeded") 
    
    # with urlopen(url) as f:
    #     return f.read()


def read_planetoid_metadata():
    url = URL_PREFIX + "PlanetoidMetadata"
    res = requestData(url, '', headers)
    metadata = PlanetoidMetadata()
    metadata.ParseFromString(res._content)
    return metadata


def read_bulk_metadata(path, epoch):
    url = URL_PREFIX + f"BulkMetadata/pb=!1m2!1s{path}!2u{epoch}"
    res = requestData(url, '', headers)
    metadata = BulkMetadata()
    metadata.ParseFromString(res._content)
    return metadata


def parse_path_and_flags(data):
    def split_bits(x, n):
        mask = (1 << n) - 1
        return x >> n, x & mask

    data, level = split_bits(data, 2)

    path_segments = list()
    for _ in range(level + 1):
        data, x = split_bits(data, 3)
        path_segments.append(x)

    path = "".join(str(x) for x in path_segments)
    return path, data


class NodeData(object):
    def __init__(self, bulk_path, path_and_flags, nodedata_epoch, imagery_epoch, metadata_epoch):
        path, flags = parse_path_and_flags(path_and_flags)
        # self.bulk_path = bulk_path
        # self.path_and_flags = path_and_flags
        self.path = bulk_path + path
        self.flags = flags
        self.level = len(self.path)
        self.nodedata_epoch = nodedata_epoch
        self.metadata_epoch = metadata_epoch
        self.imagery_epoch = imagery_epoch
        self.bbox = octant_to_latlong(self.path)
        self.bulk = (len(self.path) % 4 == 0) and (not (self.flags & 4))
   
    def is_bulk(self):
        return (len(self.path) % 4 == 0) and (not (self.flags & 4))

    def is_overlap(self, bbox):
        return LatLonBox.is_overlapping(self.bbox, bbox)


def find_overlaps(bbox, max_octants_per_level):
    planetoid_metadata = read_planetoid_metadata()
    meta_epoch = planetoid_metadata.root_node_metadata.epoch
    overlapping_octants = defaultdict(list)

    def update_overlapping_octants(path, level, meta_epoch=None):
        bulk = read_bulk_metadata(path, meta_epoch)
        bulk_path = bulk.head_node_key.path
        #overlapping_bulks[level].append(bulk)
        for node in bulk.node_metadata:
            metadata_epoch = node.bulk_metadata_epoch if node.bulk_metadata_epoch else bulk.head_node_key.epoch 
            node = NodeData(bulk_path, node.path_and_flags, node.epoch, node.imagery_epoch, metadata_epoch)
            if node.is_overlap(bbox):
                overlapping_octants[node.level].append(node)

    update_overlapping_octants("", 1, meta_epoch)
    for level in range(1, 16):
        # if len(overlapping_octants[level]) >= max_octants_per_level:
        #    break
        i = 1
        for octant in overlapping_octants[level]:
            if octant.is_bulk():
                print(f"processing {level}({i}/{len(overlapping_octants[level])})")
                update_overlapping_octants(octant.path, level, octant.metadata_epoch)        
            i+=1 
    return overlapping_octants 

def args_to_bbox(args):
    args = [float(x.rstrip(",")) for x in args]
    bottom, top = sorted([args[0], args[2]])
    left, right = sorted([args[1], args[3]])
    return LatLonBox(north=top, south=bottom, west=left, east=right)

def getGridOctants(grids):
	overlapping_octants = defaultdict(list)
	for level in range(1, len(grids)+1):
		nodes = grids[f'{level}']
		if len(nodes) > 0:
			for i in range(len(nodes)):
				n = nodes[i]
				grid = NodeData(n['bulk_path'],n['path_and_flags'], n['nodedata_epoch'], n['imagery_epoch'], n['metadata_epoch'])
				overlapping_octants[level].append(grid)
		else:
			overlapping_octants[level] = nodes
	
	return overlapping_octants
def getGrids(gridsfile):
	grids = None
	try:
		f = codecs.open(gridsfile, 'r', 'utf-8')
		s = f.read()
		f.close()

		grids = json.loads(s)
	except Exception as e:
		print(e)
	return grids

