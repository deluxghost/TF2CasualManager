# -*- coding: utf-8 -*-
import codecs
import json
import sys

class Map(object):

    def __init__(self, category, mode, data):
        self.category = category
        self.mode = mode
        self.name = data.get('name', '')
        self.bsp = data.get('bsp', '')
        self.group = data.get('group', -1)
        self.bit = data.get('bit', -1)

    def __str__(self):
        return 'Map({})'.format(self.bsp)

    def __repr__(self):
        return 'Map({})'.format(self.bsp)

def load_maps(data):
    maps = dict()
    groups = list()
    for category in data.get('categories'):
        for mode in category.get('modes'):
            for game_map in mode.get('maps'):
                map_data = Map(category['name'], mode['name'], game_map)
                bsp = map_data.bsp
                group = map_data.group
                bit = map_data.bit
                if len(groups) - 1 < group:
                    groups.extend([[] for _ in range(group - len(groups) + 1)])
                if len(groups[group]) - 1 < bit:
                    groups[group].extend([''] * (bit - len(groups[group]) + 1))
                maps[bsp] = map_data
                groups[group][bit] = bsp
    return maps, groups

def int2maps(number, group):
    flags = list(reversed('{:b}'.format(number)))
    maps = list()
    for i, flag in enumerate(flags):
        if not int(flag):
            continue
        game_map = group[i] if - len(group) <= i < len(group) else ''
        if game_map:
            maps.append(game_map)
    return maps

def maps2int(maps, maps_data):
    groups = list()
    for game_map in maps:
        m = maps_data[game_map]
        group = m.group
        bit = m.bit
        if len(groups) - 1 < group:
            groups.extend([[] for _ in range(group - len(groups) + 1)])
        if len(groups[group]) - 1 < bit:
            groups[group].extend(['0'] * (bit - len(groups[group]) + 1))
        groups[group][bit] = '1'
    groups = list(map(lambda x: ['0'] if not x else x, groups))
    groups = list(map(lambda x: int(''.join(reversed(x)), 2), groups))
    return groups

if __name__ == '__main__':
    data_file = './data/casual.min.json'
    casual = dict()
    try:
        with codecs.open(data_file, encoding='utf-8') as f:
            casual = json.loads(f.read())
    except:
        sys.exit(1)
    maps, groups = load_maps(casual)
