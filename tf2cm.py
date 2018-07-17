# -*- coding: utf-8 -*-
import codecs
import json
import os
import sys

import wx
import tf2cm_wx

__version__ = '1.0.0'

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


def int2maps(number, groups):
    flags = list(reversed('{:b}'.format(number)))
    maps = list()
    for i, flag in enumerate(flags):
        if not int(flag):
            continue
        game_map = groups[i] if - len(groups) <= i < len(groups) else ''
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

def read_casual(path, maps_data):
    pass

def write_casual(path, maps, maps_data):
    pass

def read_cm():
    pass

def write_cm(data):
    pass

def error(frame, msg):
    dlg = wx.MessageDialog(frame, msg, 'TF2CM Error', wx.ICON_ERROR)
    dlg.ShowModal()
    dlg.Destroy()
    sys.exit(1)

if __name__ == '__main__':
    app = wx.App(False)
    frame = tf2cm_wx.frameMain(None)
    icon = wx.Icon()
    icon.CopyFromBitmap(wx.Bitmap("icon.ico", wx.BITMAP_TYPE_ANY))
    frame.SetIcon(icon)
    data_file = None
    app_path = os.path.dirname(os.path.realpath(__file__))
    path = [
        os.path.join(app_path, r'data\casual.min.json'),
        os.path.join(app_path, r'data\casual.json')
    ]
    for f in path:
        if os.path.isfile(f):
            data_file = f
            break
    if not data_file:
        error(frame, 'Map selection data file not found.\nPlease re-download TF2CM.')
    casual = dict()
    try:
        with codecs.open(data_file, encoding='utf-8') as f:
            casual = json.loads(f.read())
    except:
        error(frame, 'Map selection data file is broken.\nPlease re-download TF2CM.')
    maps_data, groups = load_maps(casual)
    frame.casual = casual
    frame.maps_data = maps_data
    frame.groups = groups
    frame.load_map_struct()
    frame.SetTitle('{} {}'.format(frame.GetTitle(), __version__))
    frame.Show(True)
    app.MainLoop()
