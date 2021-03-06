# -*- coding: utf-8 -*-
import codecs
import json
import os
import sys
import traceback

import wx

import icon
import steam
import tf2cm_wx

__version__ = '1.5.1'


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


def ints2maps(numbers, groups):
    maps = list()
    for i, number in enumerate(numbers):
        if i >= len(groups):
            break
        maps.extend(int2maps(number, groups[i]))
    return maps


def maps2ints(maps, maps_data):
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


def get_path():
    if getattr(sys, 'frozen', False):
        app_path = os.path.dirname(os.path.realpath(sys.executable))
    else:
        app_path = os.path.dirname(os.path.realpath(__file__))
    return app_path


def read_casual(path, groups):
    lines = list()
    try:
        with codecs.open(path, encoding='utf-8') as f:
            lines = f.readlines()
    except:
        return False
    lines = list(map(lambda x: int(x.replace('selected_maps_bits:', '').strip()), lines))
    return ints2maps(lines, groups)


def write_casual(path, maps, maps_data):
    groups = maps2ints(maps, maps_data)
    groups = list(
        map(lambda x: 'selected_maps_bits: {}\r\n'.format(x), groups))
    try:
        with codecs.open(path, 'w', encoding='utf-8') as f:
            f.writelines(groups)
        return True
    except:
        return False


def read_cm(path=None):
    if path is None:
        path = os.path.join(get_path(), 'tf2cm.json')
    if not os.path.isfile(path):
        default_file = ''
        paths = [
            os.path.join(get_path(), r'tf2cm_default.json'),
            os.path.join(get_path(), r'data\tf2cm_default.json')
        ]
        for f in paths:
            if os.path.isfile(f):
                default_file = f
                break
        if not default_file:
            write_cm({'version': 1, 'selections': {}})
        else:
            write_cm(read_cm(f))
        return read_cm()
    with codecs.open(path, encoding='utf-8') as f:
        data = json.loads(f.read())
    return data


def write_cm(data, path=None):
    if path is None:
        path = os.path.join(get_path(), 'tf2cm.json')
    with codecs.open(path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(data, indent=None, separators=(',', ':')))


def error(frame, msg):
    dlg = wx.MessageDialog(frame, msg, 'TF2CM Error', wx.ICON_ERROR)
    dlg.ShowModal()
    dlg.Destroy()


if __name__ == '__main__':
    app = wx.App(False)
    frame = tf2cm_wx.frameMain(None)
    app_icon = wx.Icon()
    app_icon.CopyFromBitmap(icon.icon.GetBitmap())
    frame.SetIcon(app_icon)
    data_file = None
    app_path = get_path()
    frame.app_path = app_path
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
        sys.exit(1)
    casual = dict()
    try:
        with codecs.open(data_file, encoding='utf-8') as f:
            casual = json.loads(f.read())
    except:
        error(frame, 'Map selection data file is broken.\nPlease re-download TF2CM.')
        sys.exit(1)
    maps_data, groups = load_maps(casual)
    frame.casual = casual
    frame.maps_data = maps_data
    frame.groups = groups
    frame.load_map_struct()
    try:
        frame.cm = read_cm()
    except:
        error(frame, traceback.format_exc())
        sys.exit(1)
    frame.load_cm()
    frame.tf = steam.tf2()
    if not frame.tf:
        error(frame, 'TF2 is not installed properly...')
        sys.exit(1)
    frame.app_version = __version__
    frame.SetTitle('{} {}'.format(frame.GetTitle(), __version__))
    frame.Show(True)
    app.MainLoop()
