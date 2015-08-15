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
import pickle
import time

def convert_coordinates(source_coords, ak='ObH1Tg4eoPWctNEOP9RlxZKf', trans_from='1', trans_to='5', output='json'):
    '''转换坐标，默认将GPS坐标转换成百度坐标
    '''
    
    url = "http://api.map.baidu.com/geoconv/v1/?"
    parameters = {"coords": source_coords.strip(),
                "ak": ak,
                "from": trans_from,
                "to": trans_to,
                "output": output};
    
    data = urllib.parse.urlencode(parameters);
    full_url = url + data
    response = urllib.request.urlopen(full_url).read()
    response_str = response.decode("utf-8")
    result = json.loads(response_str)['result']
    # print(str(result[0]['x']) + "," + str(result[0]['y']))
    # print(repr(result))
    return result
    
        
def get_roads_coordinates(geojson_path, output_path, pickle_path = 'data.pkl'):
    '''从道路数据geojson中取出所需大路的坐标数据，生成echarts需要的格式
    Arguments:
        geojson_path    输入的json文件
        #begin_from_line_num    表示从geojson文件的第几行开始处理
        output_path    输出的echarts输入文件，json格式
        pickle_path    若出现异常，将状态信息等存到pickle文件里
    '''
    road_file = codecs.open(geojson_path, encoding='utf-8')
    
    # road_types_needed是大路的类型
    road_types_needed = set(['primary', 'tertiary', 'trunk',
        'secondary_link', 'motorway_link', 'secondary', 'trunk_link',
        'primary_link', 'motorway', 'tertiary_link', 'road'])
    
    count_processed = 0 #前一次已经处理到第几行（不包括，行数从1开始）
    count_repeat = 0    #统计用，看有多少个节点重复
    nodes_index = 0  # echarts文件里节点的编号，作为节点名
    nodes = {}  # 所有节点
    nodes_index_hashmap = {}    #查询节点编号，key=coord_gps,例如“116.3857, 39.90193”，value=node index
    roads = []  # 所选道路
    roads.append([])  # roads[0]为拥堵
    roads.append([])  # roads[1]为缓行
    roads.append([])  # roads[2]为畅通
    
    if os.path.exists(pickle_path): #若先前异常退出，则从pickle文件中获取当时的状态
        pickle_file = open(pickle_path, 'rb')
        count_processed = pickle.load(pickle_file)  
        count_repeat = pickle.load(pickle_file)
        nodes_index = pickle.load(pickle_file)
        nodes = pickle.load(pickle_file)
        nodes_index_hashmap = pickle.load(pickle_file)
        roads = pickle.load(pickle_file)
        pickle_file.close()

    count = 0
    try:    #防止断开连接异常
        for line in road_file:
            count += 1
            if count < count_processed: #若先前异常前已处理过了，就跳过
                continue
            
            if(count % 100 == 0):
                print(count)
                print("node_index:" + str(nodes_index))
                print("count_repeat:" + str(count_repeat))
                
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
                    
                    #quiry_result = []
                    quiry_result = convert_coordinates(coord_gps_param)
 
                    # print(repr(quiry_result))
                    coordinates_baidu = []
                    # 获取百度坐标列表
                    for node in quiry_result:
                        coordinates_baidu.append([round(node['x'], 5), round(node['y'], 5)])
                   
                    # print(repr(coordinates_baidu))
                    road_status = random.randint(0, 2)  # 随机道路状态
                    node_index_last = 0    #用来记下要连线的前一个点的索引
                    node_index_now = 0  #用来记下当前节点的索引
                    for index in range(len(coordinates_baidu)):
                        coord_baidu_str = str(coordinates_baidu[index][0]) + "," + str(coordinates_baidu[index][1])
                        quiry_index = nodes_index_hashmap.get(coord_baidu_str, -1)
                        if  quiry_index == -1:
                            #当前节点未出现过，新存储一个
                            nodes_index += 1
                            node_index_now = nodes_index
                            nodes[str(node_index_now)] = coordinates_baidu[index]
                            nodes_index_hashmap[coord_baidu_str] = nodes_index
                        else:   #节点已出现过，查之前出现的索引
                            count_repeat += 1
                            node_index_now = quiry_index
    
                        if (index != 0) :
                            # fragment是一个线路片段
                            fragment = []
                            fragment_head = {}
                            fragment_head["name"] = str(node_index_last)
                            fragment_tail = {}
                            fragment_tail["name"] = str(node_index_now)
                            fragment.append(fragment_head)
                            fragment.append(fragment_tail)
                            roads[road_status].append(fragment)
                        
                        node_index_last = node_index_now
                    # nodes[str(nodes_index)] = coordinates_baidu[len(coordinates_baidu) - 1]
        
        print("\nsuccess!")
        print("nodes_num:" + str(nodes_index))
        print("count_repeat:" + str(count_repeat))
        
        
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
    
    except Exception as e:
        print(e)
        print("异常 at line:" + str(count))
        try:
            if os.path.exists(pickle_path):
                os.remove(pickle_path)  #先删除原有pickle文件
        except Exception as e:
            print(e)
        pickle_file = open(pickle_path, 'wb')
        pickle.dump(count, pickle_file)
        pickle.dump(count_repeat, pickle_file)
        pickle.dump(nodes_index, pickle_file)
        pickle.dump(nodes, pickle_file)
        pickle.dump(nodes_index_hashmap, pickle_file)
        pickle.dump(roads, pickle_file)
        pickle_file.close()
        print("已保存状态到pickle文件")
        return 0
    finally:
        road_file.close()
        
    return 1


def test():
    pass

def main():
    #test()
    
    
    #os.remove('data.pkl')
    ret = 0
    while(ret != 1):
        ret = get_roads_coordinates("./GetBaiduCoordinates/BeijingRoads.json", "./GetBaiduCoordinates/data.json", "./GetBaiduCoordinates/data.pkl")
        if ret == 0:
            time.sleep(60)
    
if __name__ == "__main__":
    main()


