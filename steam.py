# -*- coding: utf-8 -*-
import os
import re
import winreg

def tf2():
    vdf_pat = re.compile(r'^\s*"\d+"\s*".+"\s*')
    steam = None
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Valve\Steam') as handle:
            steam = winreg.QueryValueEx(handle, 'SteamPath')[0].replace('/', '\\')
    except:
        return None
    libs = [steam]
    libinfo = os.path.join(steam, r'steamapps\libraryfolders.vdf')
    try:
        with open(libinfo, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if vdf_pat.match(line):
                    libs.append(line.split()[1].strip('"').replace('\\\\', '\\'))
    except:
        pass
    for lib in libs:
        find_acf = os.path.join(lib, r'steamapps\appmanifest_440.acf')
        if os.path.isfile(find_acf):
            tf_root = os.path.join(lib, r'steamapps\common\Team Fortress 2\tf')
            if os.path.isdir(tf_root):
                return tf_root
    return None
