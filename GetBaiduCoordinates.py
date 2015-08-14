# -*- coding: UTF-8 -*-
'''
Created on 2015年8月13日

@author: lwt

python version: 3.4
'''

import os
import urllib
import urllib.parse
import urllib.request
import json
import codecs
import random
    

def convert_coordinates(source_coords, ak='ObH1Tg4eoPWctNEOP9RlxZKf', trans_from='1', trans_to='5', output='json'):
    '''转换坐标，默认将GPS坐标转换成百度坐标
    '''
    
    url = "http://api.map.baidu.com/geoconv/v1/?"
    parameters = {"coords": source_coords.strip(),
                "ak": ak,
                "from": trans_from,
                "to": trans_to,
                "output": output};
    try:
        
        data = urllib.parse.urlencode(parameters);
        full_url = url + data
        response = urllib.request.urlopen(full_url).read()
        response_str = response.decode("utf-8")
        result = json.loads(response_str)['result']
        # print(str(result[0]['x']) + "," + str(result[0]['y']))
        # print(repr(result))
        return result
    except Exception as e:
        print(e)
        
def get_roads_coordinates(geojson_path, output_path):
    '''从道路数据geojson中取出所需大路的坐标数据，生成echarts需要的格式
    Arguments:
        geojson_path    输入的json文件
        output_path    输出的echarts输入文件，json格式
    '''
    road_file = codecs.open(geojson_path, encoding='utf-8')
    
    # road_types_needed是大路的类型
    road_types_needed = set(['primary', 'tertiary', 'trunk',
        'secondary_link', 'motorway_link', 'secondary', 'trunk_link',
        'primary_link', 'motorway', 'tertiary_link', 'road'])
    nodes = {}  # 所有节点
    nodes_index = 0  # echarts文件里节点的编号，作为节点名
    roads = []  # 所选道路
    roads.append([])  # roads[0]为拥堵
    roads.append([])  # roads[1]为缓行
    roads.append([])  # roads[2]为畅通
    count = 0
    for line in road_file:
        count += 1
        print(count)
        if(count > 1000):
            break
        if (line.startswith("{ \"type\": \"Feature\", \"properties\": { \"osm_id\"")):  # 以这个作为道路行数据的标志
            if(line.endswith(',\n')):
               line = line.rstrip(', \n')  # 去除末尾可能有的逗号
            road_data = json.loads(line)
            # properties = road_data['properties']
            # road_type = properties['type']
            if (road_data['properties']['type'] in road_types_needed):  # 只取出大路
               coordinates_gps = road_data['geometry'] ['coordinates']
               coord_gps_param = ''
               # 转换坐标
               for coord in coordinates_gps:
                   if len(coord_gps_param) == 0:
                       coord_gps_param = str(coord[0]) + ',' + str(coord[1])
                   else:
                       coord_gps_param = coord_gps_param + ';' + str(coord[0]) + ',' + str(coord[1])
                        
               quiry_result = convert_coordinates(coord_gps_param)
               # print(repr(quiry_result))
               coordinates_baidu = []
               # 获取百度坐标列表
               for node in quiry_result:
                   coordinates_baidu.append([node['x'], node['y']])
               
               # print(repr(coordinates_baidu))
               road_status = random.randint(0, 2)  # 随机道路状态
               for index in range(len(coordinates_baidu)):
                   if (index != len(coordinates_baidu) - 1) :
                       # fragment是一个线路片段
                       fragment = []
                       fragment_head = {}
                       fragment_head["name"] = str(nodes_index)
                       fragment_tail = {}
                       fragment_tail["name"] = str(nodes_index + 1)
                       fragment.append(fragment_head)
                       fragment.append(fragment_tail)
                       roads[road_status].append(fragment)
                   
                   nodes[str(nodes_index)] = coordinates_baidu[index]
                   nodes_index += 1
               # nodes[str(nodes_index)] = coordinates_baidu[len(coordinates_baidu) - 1]
    print("nodes_num:" + str(nodes_index))
    
    road_file.close()
    
    output_file = codecs.open(output_path, mode='w', encoding='utf-8')
    output = {}
    output["traffic_data"] = {}
    output["traffic_data"]["nodes_geoCoord"] = nodes
    output["traffic_data"]["jam_line"] = roads[0]
    output["traffic_data"]["slow_line"] = roads[1]
    output["traffic_data"]["quick_line"] = roads[2]
    output_str = json.dumps(output)
    output_file.write(output_str)
    output_file.close()

def get_roads_coordinates_evaluate(geojson_path, output_path):
    '''从道路数据geojson中取出所需大路的坐标数据，生成echarts需要的格式
    Arguments:
        geojson_path    输入的json文件
        output_path    输出的echarts输入文件，json格式
    '''
    road_file = codecs.open(geojson_path, encoding='utf-8')
    
    # road_types_needed是大路的类型
    road_types_needed = set(['primary', 'tertiary', 'trunk',
        'secondary_link', 'motorway_link', 'secondary', 'trunk_link',
        'primary_link', 'motorway', 'tertiary_link', 'road'])
    nodes = {}  # 所有节点
    nodes_index = 0  # echarts文件里节点的编号，作为节点名
    roads = []  # 所选道路
    roads.append([])  # roads[0]为拥堵
    roads.append([])  # roads[1]为缓行
    roads.append([])  # roads[2]为畅通
    count = 0
    nodes_set = set()
    count_repeat = 0
    for line in road_file:
        count += 1
        #print(count)
        #if(count > 1000):
            #break
        if (line.startswith("{ \"type\": \"Feature\", \"properties\": { \"osm_id\"")):  # 以这个作为道路行数据的标志
            if(line.endswith(',\n')):
                line = line.rstrip(', \n')  # 去除末尾可能有的逗号
            road_data = json.loads(line)
            # properties = road_data['properties']
            # road_type = properties['type']
            if (road_data['properties']['type'] in road_types_needed):  # 只取出大路
                coordinates_gps = road_data['geometry'] ['coordinates']
                for coord in coordinates_gps:
                    
                    coord_str = str(coord[0]) + ',' + str(coord[1]) 
                    if coord_str in nodes_set:
                        count_repeat += 1
                        print (count_repeat)
                    else:
                        nodes_set.add(coord_str);
    print(count_repeat)

def main():

    #get_roads_coordinates("BeijingRoads.json", "data.json")
    get_roads_coordinates_evaluate("BeijingRoads.json", "data.json")
    # convert_coordinates("116.29966, 39.96912;116.29966, 39.96912" )
    
    
    
if __name__ == "__main__":
    main()



