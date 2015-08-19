# -*- coding: UTF-8 -*-
'''
Created on 2015年8月16日

@author: lwt

python version: 3.4
'''
#此脚本用于生成PowerReliability.html中所需的数据


import random
import codecs
import json


def create_node(name, category, item_style = 'default', value = 0):
    node = {}
    node['name'] = name
    if value != 0:
        node_value = round(value * 100, 2)
        node['value'] = str(node_value) + '%'
    else:   #随机
        node_value = round(random.uniform(95, 98), 2)
        node['value'] = str(node_value) + '%'
    node['category'] = category
    if item_style != 'default':
        node['itemStyle'] = item_style
    else:
        node['itemStyle'] = {}
        node['itemStyle']['normal'] = {}
        node['itemStyle']['normal']['label'] = {}
        if name != "北京市":
            node['itemStyle']['normal']['label']['show'] = "false" #默认不显示,此处注意，生成的json文件里面会是"true"，但这样不行，把json文件里面的“true”改成不带引号的
        else:
            node['itemStyle']['normal']['label']['show'] = "true"
        # 根据值设置不同颜色
        if node_value > 97: #97-98
            node['itemStyle']['normal']['color'] = "#FFFF00"
        elif node_value > 96:   #96-97
            node['itemStyle']['normal']['color'] = "#FF8000"
        elif node_value > 95:   #95-96
            node['itemStyle']['normal']['color'] = "#FF0000"
    
    if category == 0:
        node['symbolSize'] = 10
    elif category == 1:
        node['symbolSize'] = 6
    elif category == 2:
        node['symbolSize'] = 3
    return node

def create_link(source, target, weight = 1):
    link = {}
    link['source'] = source
    link['target'] = target
    link['weight'] = weight
    return link

def make_power_reliability_data(output_path):
    '''产生PowerReliability所需数据
    Arguments:
        output_path    输出json文件路径
    '''
    data = {}
    data['nodes'] = []
    data['links'] = []
    data['categories'] = []
    nodes = data['nodes']
    links = data['links']
    categories = data['categories']
    '''
    categories.append({"name":"市"})
    categories.append({"name":"区县"})
    categories.append({"name":"乡镇、地区"})
    '''
    categories.append({"name":"0"})
    categories.append({"name":"1"})
    categories.append({"name":"2"})
    
    districts = ["密云县", "怀柔区", "房山区", "延庆县", "门头沟区",
                 "昌平区", "大兴区", "顺义区", "平谷区", "通州区",
                 "朝阳区", "海淀区", "丰台区", "石景山区", "西城区", 
                 "东城区", "宣武区", "崇文区"]
    nodes.append(create_node('北京市', 0))
    for district in districts:
        nodes.append(create_node(district, 1))
        links.append(create_link('北京市', district))
        
        if district == '海淀区':
            nodes.append(create_node('北大', 2))
            links.append(create_link('海淀区', '北大'))
            nodes.append(create_node('中关村', 2))
            links.append(create_link('海淀区', '中关村'))
            nodes.append(create_node('上地', 2))
            links.append(create_link('海淀区', '上地'))
            nodes.append(create_node('清河', 2))
            links.append(create_link('海淀区', '清河'))
        elif district == '朝阳区':
            nodes.append(create_node('望京', 2))
            links.append(create_link('朝阳区', '望京'))
            nodes.append(create_node('花家地', 2))
            links.append(create_link('朝阳区', '花家地'))
            nodes.append(create_node('燕莎', 2))
            links.append(create_link('朝阳区', '燕莎'))
        else:
            for i in range(random.randint(3, 5)):
                area_name = district + str(i)
                nodes.append(create_node(area_name, 2))
                links.append(create_link(district, area_name))
            
        
    output_file = codecs.open(output_path, encoding='utf-8', mode='w')
    output_file.write(json.dumps(data, ensure_ascii=False, indent=4))
    
def test():
    pass
    
if __name__ == '__main__':
    #test()
    make_power_reliability_data('./MakePowerReliabilityData/data.json')