# -*- coding: UTF-8 -*-
'''
Created on 2015年8月15日

@author: lwt

python version: 3.4
'''

import json
import codecs
import sys
import os
import imp




def get_range(geometry):
    range = [180, 0, 90, 0]     #[经度下限，经度上限，纬度下限，纬度上限]
    if (geometry['type'] == "Polygon"):
        points = geometry['coordinates'][0]
    elif(geometry['type'] == 'MultiPolygon'):
        points = []
        for polygon in geometry['coordinates']:
            points = points + polygon[0]
    
    
    for point in points:
        if point[0] < range[0]:
            range[0] = point[0]
        if point[0] > range[1]:
            range[1] = point[0]
        if point[1] < range[2]:
            range[2] = point[1]
        if point[1] > range[3]:
            range[3] = point[1]
    return range

def get_beijing_range(beijing_map_path = './GetBeijingRange/beijing-map.json'):
    
    map_file = codecs.open(beijing_map_path, encoding='utf-8')
    strs = ""
    for line in map_file:
        strs = strs + line
    map_json = json.loads(strs)
    
    map_features = map_json['features']
    beijing_range_json = {}
    for map_feature in map_features:
        
        range = get_range(map_feature['geometry'])
        properties = map_feature['properties']
        beijing_range_json[properties['name']] = {'id':properties['id'], 'cp':properties['cp'], 'range':range}
        
    file = codecs.open("./GetBeijingRange/beijing_range.json", encoding='utf-8', mode = 'w')
    json.dump(beijing_range_json, file, ensure_ascii=False, indent=4)
    file.close()


if __name__ == '__main__':
    
    get_beijing_range()