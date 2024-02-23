#!/usr/bin/env python 
# coding:utf-8

import gzip
import sys
import traceback
import json
import os
import argparse
import copy
import urllib
from collections import defaultdict, OrderedDict
from io import StringIO
from urllib.parse import urlparse
from urllib.request import urlretrieve
import urllib.request
import codecs
import socket
import base64


class GridData(object):
    def __init__(self, path, nodedata_epoch, imagery_epoch, metadata_epoch, bulk):
        self.path = path
        self.level = len(self.path)
        self.nodedata_epoch = nodedata_epoch
        self.metadata_epoch = metadata_epoch
        self.imagery_epoch = imagery_epoch
        self.bulk = bulk

class CKey(object):
	keylist = None
	cur_indx = 0
	current = None
	rootURL = None
	query = None
	path = None

	def __init__(self, keylist, rootURL):
		self.keylist = keylist
		self.cur_indx = 0
		self.current = keylist[self.cur_indx]
		self.rootURL = rootURL
		self.newsession()

	def switch(self):
		key_num = len(self.keylist)
		if key_num > 1:
			self.cur_indx = (self.cur_indx + 1) % key_num
			self.current = keylist[self.cur_indx]
		
	def getkey(self):
		return self.current
	
	def newsession(self):
		url = self.rootURL + '?key='+ self.current
		response = urllib.request.urlopen(url)
		tileset =json.loads(response.read().decode('utf-8'))
		nodeData = tileset['root']
		uri = nodeData['children'][0]['children'][0]['content']['uri']
		uu = urlparse(uri)
		self.query = uu.query
		self.path = uu.path[0:(uu.path.rfind('/')+1)]

	def getsession(self):
		return self.query
	
	def getpath(self):
		return self.path
	
socket.setdefaulttimeout(300)
#解析获取的根json文件，提取senssion id
#{"asset":{"version":"1.0"},"geometricError":1e+100,"root":{"boundingVolume":{"box":[0,0,0,7972671.25,0,0,0,7972671.25,0,0,0,7945940.3928064629]},
# "geometricError":1e+100,
# "refine":"REPLACE",
# "transform":[1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1],
# "children":[
# {"boundingVolume":{"box":[0,0,0,7972671.25,0,0,0,7972671.25,0,0,0,7945940.3928064629]},
# "geometricError":1e+100,
# "refine":"REPLACE",
# "children":[
# {"boundingVolume":{"box":[0,0,0,7972671.25,0,0,0,7972671.25,0,0,0,7945940.3928064629]},
# "geometricError":1e+100,
# "content":{
# "uri":"/v1/3dtiles/datasets/CgA/files/UlRPVEYuYnVsa21ldGFkYXRhLnBsYW5ldG9pZD1lYXJ0aCxidWxrX21ldGFkYXRhX2Vwb2NoPTk1MyxwYXRoPSxjYWNoZV92ZXJzaW9uPTY.json?session=CMzK6LndoeendxDEr92lBg"
# }}],"extras":{"comment":"path = ''"}}]},"extensionsUsed":["3DTILES_content_gltf"],"extensionsRequired":["3DTILES_content_gltf"]}
def getSessionParams(key, url):
	url = url + '?key='+ key.getkey()
	response = urllib.request.urlopen(url)
	tileset =json.loads(response.read().decode('utf-8'))
	nodeData = tileset['root']
	uri = nodeData['children'][0]['children'][0]['content']['uri']
	uu = urlparse(uri)
	path = uu.path[0:(uu.path.rfind('/')+1)]
	#query = uu.query[uu.query.find('=')+1:len(uu.query)]
	return uu.query, path

# 获取Json记录的瓦片文件
def getContentsOfGLB(contents, n):
	# 下载content url里的东西
	if n.get('content') is not None:
		c = n['content']
		if c.get('uri') is not None:
			if c['uri'].find(".glb") > -1:
				contents.append(c['uri'])

	if n.get('children') is not None:
		children = n['children']
		for i in range(len(children)):
			c = children[i]
			getContentsOfGLB(contents, c) 
	return	

# 获取Json文件八叉树文件
def getContentsJson(contents, n):
	# 下载content url里的东西
	if n.get('content') is not None:
		c = n['content']
		if c.get('uri') is not None:
			if c['uri'].find(".json") > -1:
				if c['uri'] not in contents:
					contents.append(c['uri'])

	if n.get('children') is not None:
		children = n['children']
		for i in range(len(children)):
			c = children[i]
			getContentsJson(contents, c) 
	return

def getContentsAll(contents, n):
	# 下载content url里的东西
	if n.get('content') is not None:
		c = n['content']
		if c.get('uri') is not None:
			if c['uri'].find(".json") > -1 or c['uri'].find(".glb") > -1:
				if c['uri'] not in contents:
					contents.append(c['uri'])

	if n.get('children') is not None:
		children = n['children']
		for i in range(len(children)):
			c = children[i]
			getContentsAll(contents, c) 
	return

def gzdecode(data):
	# with patch_gzip_for_partial():
	compressedStream = StringIO(data)
	gziper = gzip.GzipFile(fileobj=compressedStream)
	data2 = gziper.read()

	# print(len(data))
	return data2

def autoDownLoad(url, add, overwrite = False):
	errcode = 0
	try:
		if os.path.exists(add) and not overwrite:
			return 0
		# a表示地址， b表示返回头
		# 下载以后的数据可能是经过压缩的，我们只需要根据返回头判断是否需要解压缩即可，
		# 但因为urlretrieve会直接将远程数据下载到本地。所以我们需要对本地数据进行二次处理。
		a, b = urlretrieve(url, add)
		keyMap = dict(b)
		if 'content-encoding' in keyMap and keyMap['content-encoding'] == 'gzip':
			#or keyMap['content-encoding'] == 'application/json'):
			#print('need2be decode')
			objectFile = open(add, 'rb+')  # 以读写模式打开
			data = objectFile.read()
			data = gzdecode(data)
			objectFile.seek(0, 0)
			objectFile.write(data)
			objectFile.close()

		if os.stat(add).st_size == 0:
			errcode = 6
			return errcode  #文件大小为0， 下载失败
		
		return 0
		
	except urllib.error.ContentTooShortError:
		print('Network conditions is not good.Reloading.')
		autoDownLoad(url, add)
	except socket.timeout:
		print('fetch ', url, ' exceedTime ')
		try:
			urlretrieve(url, add)
		except:
			print('reload failed')
			errcode = 1
	except urllib.error.HTTPError as e:
		if e.code == 429:
			print('too many request!!!')
			errcode = 2
		elif e.code == 400:
			print('session timeout!!!')
			errcode = 3
		else:
			errcode = 128
	except FileNotFoundError:
		errcode = 4	#文件不存在，下载失败
	except:
		traceback.print_exc()
		errcode = 5
	return errcode

def downloadList(baseurl, savedir, key, contentsALL, failedlist):
	# for i in range(start, len(contentsJson)):
	i = 0
	while i < len(contentsALL):
		query = key.getsession()
		c = contentsALL[i]
		file = savedir + '/' + c
		dirname = os.path.dirname(file)
		if not os.path.exists(dirname):
			os.makedirs(dirname)

		url = baseurl + c + '?' + query + '&key=' + key.getkey()
		#url = uu.scheme + "://" + uu.netloc + c.uri + '?' + uu.query
		code = autoDownLoad(url, file)
		if not code:
			print('[' + query + ', key=' + key.getkey() + ']' + c.split("/")[-1] + ' download success: ' +
				  str(i+1) + '/' + str(len(contentsALL)))
		else:
			if code == 2: #reach Maximum 250,000 renderer’s tile requests per day
				key.switch()
			elif code == 3: #session timeout
				key.newsession()
			else:
				print('ErrCode:' + str(code))

			print('[' + query + ', key=' + key.getkey() + ']' + c.split("/")[-1] + ' download failed: ' +
				  str(i+1) + '/' + str(len(contentsALL)))
			failedlist.append(c)
		i+=1
	return len(failedlist)

def downloadCycle(baseurl, savedir,  key, contentsALL, failedlist):
	# for i in range(start, len(contentsJson)):
	i = 0
	while i < len(contentsALL):
		query = key.getsession()
		c = contentsALL[i]
		file = savedir + '/' + c
		dirname = os.path.dirname(file)
		if not os.path.exists(dirname):
			os.makedirs(dirname)

		url = baseurl + c + '?' + query + '&key=' + key.getkey()
		#url = uu.scheme + "://" + uu.netloc + c.uri + '?' + uu.query
		code = autoDownLoad(url, file)
		if not code:
			print('[' + query + ', key=' + key.getkey() + ']' + c.split("/")[-1] + ' download success: ' +
				  str(i+1) + '/' + str(len(contentsALL)))
			if c.endswith('.json'):
				# 解析
				tileset = getTileset(file)
				getContentsAll(contentsALL, tileset['root'])
		else:
			if code == 2:
				key.switch()
			elif code == 3:
				key.newsession()
			else:
				print('ErrCode:' + str(code))
			print('[' + query + ', key=' + key.getkey() + ']' + c.split("/")[-1] + ' download failed: ' +
				  str(i+1) + '/' + str(len(contentsALL)))
			failedlist.append(c)
		i+=1
	return len(failedlist)

def getTileset(tilesetfile):
	tileset = None
	try:
		f = codecs.open(tilesetfile, 'r', 'utf-8')
		s = f.read()
		f.close()

		tileset = json.loads(s)
	except Exception as e:
		print(e)
	return tileset

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

def getGridOctants(grids):
	overlapping_octants = defaultdict(list)
	for level in range(1, len(grids)+1):
		nodes = grids[f'{level}']
		if len(nodes) > 0:
			for i in range(len(nodes)):
				n = nodes[i]
				grid = GridData(n['path'], n['nodedata_epoch'], n['imagery_epoch'], n['metadata_epoch'], n['bulk'])
				overlapping_octants[level].append(grid)
		else:
			overlapping_octants[level] = nodes
	
	return overlapping_octants


def parse_args():
    description = "usage: % prog[options]"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-k', '--key', nargs='+', default=['AIzaSyBihOYEcycPL4u1UZBzboCr3Ql4AaZgrQk','AIzaSyAg3kvtU6wh1BTxO0or_5hovV6YJV-m-LQ','AIzaSyC9BsFXN7nV2uNlPjk3TfAArSA5FiJOBvc','AIzaSyD-sJKuhCVqR6bpkRWBgTyxnszApF9_U-M','AIzaSyD4HU7Yy05pTAodFGXEjHaXc49YbBCJstg'], help='google map token key')
    parser.add_argument('-d', '--dir', required=True, help='The directory for saving map 3dtiles')
    parser.add_argument('-g', '--grid', required=True, help='The grid config for map of selected area')
 
    args = parser.parse_args()
    return args


if __name__ == "__main__":
	args = parse_args()
	keylist = args.key
	savedir = args.dir
	gridsfile = args.grid
	rootURL = 'https://tile.googleapis.com/v1/3dtiles/root.json'
	key = CKey(keylist, rootURL)
	
	query = key.getsession()
	path = key.getpath()
	# query, path = getSessionParams(key, rootURL)
	if query == '' or path == '':
		print('Could not get session id, please check network or token key!')
		sys.exit(2)

	if os.path.isfile(savedir):
		print('savedir can not be a file ', savedir)
		sys.exit(2)

	if not os.path.exists(savedir+path):
		os.makedirs(savedir+path)

	if not os.path.exists(savedir):
		os.makedirs(savedir)

	gridsjosn = getGrids(gridsfile)
	octants = getGridOctants(gridsjosn['grids'])

	
	for level in sorted(octants):
		print(f"[Octant level {level}]")
		for octant in sorted(octants[level], key=lambda x: x.path):
			print(f"path: {octant.path} " + f"metadata_epoch: {octant.metadata_epoch}" + f"nodedata_epoch: {octant.nodedata_epoch} " + f"imagery_epoch: {octant.imagery_epoch}")
	
	uu = urlparse(rootURL)
	opener = urllib.request.build_opener()
	opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')]
	urllib.request.install_opener(opener)
	bRootTileset = False
	contentFailed = []
	# Download the root.json by default
	access_str = 'RTOTF.bulkmetadata.planetoid=earth,bulk_metadata_epoch=959,path=,cache_version=6'
	filename = base64.urlsafe_b64encode(access_str.encode()).decode().rstrip('=') + '.json'
	tileseturl = uu.scheme + "://" + uu.netloc + path + filename + '?' + key.getsession() + '&key=' + key.getkey()
	tilesetfile = savedir + path + "tileset.json"
	if autoDownLoad(tileseturl, tilesetfile, True):
		print('download ' + filename + ' failed')
		sys.exit(2)
	else:
		print('download ' + filename + ' success')	

	#解析json文件
	tileset = getTileset(tilesetfile)
	contentsGLB = []
	getContentsOfGLB(contentsGLB, tileset['root'])
	downloadList(uu.scheme + "://" + uu.netloc, savedir, key, contentsGLB, contentFailed)
	#下载该json文件中的json文件
	#contentsJson = []
	#getContentsJson(contentsJson, tileset['root'])
	#downloadList(uu.scheme + "://" + uu.netloc, savedir, key, contentsJson, contentFailed)

	for level in sorted(octants):
		i = 0
		for octant in octants[level]:
			print(f"[Bulk level: {level}({i+1}/{len(octants[level])}), path: {octant.path}]")
			if octant.imagery_epoch != 0:
				access_str = 'RTOTF.nodedata.planetoid=earth,node_data_epoch=' + f'{octant.nodedata_epoch}' + ',path=' + f'{octant.path}' + ',cache_version=6,imagery_epoch=' + f'{octant.imagery_epoch}'  
				filename = base64.urlsafe_b64encode(access_str.encode()).decode().rstrip('=') + '.glb'
				tileseturl = uu.scheme + "://" + uu.netloc + path + filename + '?' + key.getsession() + '&key=' + key.getkey() 
				tilesetfile = savedir + path + filename
				code = autoDownLoad(tileseturl, tilesetfile)
				if code:
					if code == 2:
						key.switch()
					contentFailed.append(path + filename)
					print('download ' + filename + ' failed')
				else:
					print('download ' + filename + ' success')
			if octant.bulk:
				access_str = 'RTOTF.bulkmetadata.planetoid=earth,bulk_metadata_epoch=' + f'{octant.metadata_epoch}' + ',path=' + f'{octant.path}' + ',cache_version=6'
				filename = base64.urlsafe_b64encode(access_str.encode()).decode().rstrip('=') + '.json'
				tileseturl = uu.scheme + "://" + uu.netloc + path + filename + '?' + key.getsession() + '&key=' + key.getkey()
				print(tileseturl)
				if len(octants[level]) == 1:
					if level+4 <= len(octants):
						if len(octants[level+4]) == 1:
							continue
					tilesetfile = savedir + path + "tileset.json"
					if autoDownLoad(tileseturl, tilesetfile, True):
						print('download ' + filename + ' failed')
						sys.exit(2)
					else:
						print('download ' + filename + ' success')	
				
				tilesetfile = savedir + path + filename
				code = autoDownLoad(tileseturl, tilesetfile)
				if code:
					if code == 2:
						key.switch()
					contentFailed.append(path + filename)
					print('download ' + filename + ' failed')
				else:
					print('download ' + filename + ' success')	
					#解析json文件
					tileset = getTileset(tilesetfile)
					if len(octants) > level:   #非最底层，只下载本json文件包含的子json和glb文件
						contentsGLB = []
						getContentsOfGLB(contentsGLB, tileset['root'])
						downloadList(uu.scheme + "://" + uu.netloc, savedir, key, contentsGLB, contentFailed)
						#下载该json文件中的json文件
						contentsJson = []
						getContentsJson(contentsJson, tileset['root'])
						downloadList(uu.scheme + "://" + uu.netloc, savedir, key, contentsJson, contentFailed)
					else:	#递归下载该json文件中所有json和glb
						contentsGLB = []
						getContentsOfGLB(contentsGLB, tileset['root'])
						downloadList(uu.scheme + "://" + uu.netloc, savedir, key, contentsGLB, contentFailed)
						contentsALL = []
						getContentsJson(contentsALL, tileset['root'])
						downloadCycle(uu.scheme + "://" + uu.netloc, savedir, key, contentsALL, contentFailed)
			i += 1

	# 最后处理下载过程中失败的文件
	failedList = []
	while len(contentFailed) > 0:
		downloadCycle(uu.scheme + "://" + uu.netloc, savedir,  key, contentFailed, failedList)
		if len(failedList) > 0:
			contentFailed = copy.deepcopy(failedList)
			failedList = []
		else:
			break

	print("Download Finished")


	
