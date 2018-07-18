# -*- coding: utf-8 -*-
import os

import wx
import wx.lib.agw.customtreectrl as CT
import wx.xrc

import tf2cm


class CustomTree(CT.CustomTreeCtrl):

    def __init__(self, parent, *args, **kw):
        CT.CustomTreeCtrl.__init__(self, parent, *args, **kw)

    def AutoCheckParent(self, item, checked):
        parent = item.GetParent()
        if not parent or parent.GetType() != 1:
            return
        if checked:
            child, cookie = self.GetFirstChild(parent)
            while child:
                if child.GetType() == 1 and child.IsEnabled():
                    if checked == child.IsChecked():
                        self.CheckItem2(parent, checked, torefresh=True)
                        self.AutoCheckParent(parent, checked)
                        return
                child, cookie = self.GetNextChild(parent, cookie)
        else:
            child, cookie = self.GetFirstChild(parent)
            while child:
                if child.GetType() == 1 and child.IsEnabled():
                    if checked != child.IsChecked():
                        return
                child, cookie = self.GetNextChild(parent, cookie)
            self.CheckItem2(parent, checked, torefresh=True)
            self.AutoCheckParent(parent, checked)

    def GetCheckedItems(self, parent=None, checked=None):
        if parent is None:
            parent = self.GetRootItem()
        if checked is None:
            checked = []
        child, cookie = self.GetFirstChild(parent)
        while child:
            if self.IsItemChecked(child):
                checked.append(child)
            checked = self.GetCheckedItems(child, checked)
            child, cookie = self.GetNextChild(parent, cookie)
        return checked

    def CollapseAll(self, parent=None):
        if parent is None:
            parent = self.GetRootItem()
        child, cookie = self.GetFirstChild(parent)
        while child:
            self.CollapseAll(child)
            self.Collapse(child)
            child, cookie = self.GetNextChild(parent, cookie)
        self.Collapse(parent)

    def GetAllItems(self, itemParent=None, Items=None):
        if itemParent is None:
            itemParent = self.GetRootItem()
        if Items is None:
            Items = []
        child, cookie = self.GetFirstChild(itemParent)
        while child:
            Items.append(child)
            Items = self.GetAllItems(child, Items)
            child, cookie = self.GetNextChild(itemParent, cookie)
        return Items

    def GetMaps(self):
        maps = self.GetCheckedItems()
        maps = list(map(lambda x: self.GetPyData(x), maps))
        maps = [m for m in maps if m is not None]
        return maps

    def SetMaps(self, maps):
        items = [i for i in self.GetAllItems() if self.GetPyData(i)
                 is not None]
        for m in items:
            if self.GetPyData(m) in maps:
                self.CheckItem(m)
            else:
                self.CheckItem(m, False)


class frameMain(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title='TF2 Casual Manager', pos=wx.DefaultPosition, size=wx.Size(
            540, 480), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.Size(480, 320), wx.DefaultSize)
        self.SetBackgroundColour(
            wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE))

        self.bSizerMain = wx.BoxSizer(wx.HORIZONTAL)

        self.bSizerLeft = wx.BoxSizer(wx.VERTICAL)

        self.staticGroups = wx.StaticText(
            self, wx.ID_ANY, 'Map Groups:', wx.DefaultPosition, wx.DefaultSize, 0)
        self.staticGroups.Wrap(-1)
        self.bSizerLeft.Add(self.staticGroups, 0, wx.ALL | wx.EXPAND, 5)

        listboxGroupChoices = []
        self.listboxGroup = wx.ListBox(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                       listboxGroupChoices, wx.LB_NEEDED_SB | wx.LB_SINGLE | wx.LB_SORT)
        self.bSizerLeft.Add(self.listboxGroup, 1, wx.ALIGN_TOP |
                       wx.ALL | wx.EXPAND, 5)

        gSizerButtons = wx.GridSizer(2, 2, 0, 0)

        self.buttonAdd = wx.Button(
            self, wx.ID_ANY, 'Add Group', wx.DefaultPosition, wx.DefaultSize, 0)
        gSizerButtons.Add(self.buttonAdd, 0, wx.ALIGN_CENTER |
                          wx.ALL | wx.EXPAND, 5)

        self.buttonDelete = wx.Button(
            self, wx.ID_ANY, 'Delete Group', wx.DefaultPosition, wx.DefaultSize, 0)
        gSizerButtons.Add(self.buttonDelete, 0,
                          wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 5)

        self.buttonSave = wx.Button(
            self, wx.ID_ANY, 'Save Group', wx.DefaultPosition, wx.DefaultSize, 0)
        gSizerButtons.Add(self.buttonSave, 1,
                          wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 5)

        self.buttonApply = wx.Button(
            self, wx.ID_ANY, 'Apply to TF2', wx.DefaultPosition, wx.DefaultSize, 0)
        gSizerButtons.Add(self.buttonApply, 0,
                          wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 5)

        self.bSizerLeft.Add(gSizerButtons, 0, wx.ALIGN_BOTTOM |
                       wx.EXPAND, 5)

        self.bSizerMain.Add(self.bSizerLeft, 1, wx.EXPAND, 5)

        self.bSizerRight = wx.BoxSizer(wx.VERTICAL)

        self.bSizerGroupName = wx.BoxSizer(wx.HORIZONTAL)

        self.staticGroupName = wx.StaticText(
            self, wx.ID_ANY, 'Group:', wx.DefaultPosition, wx.DefaultSize, 0)
        self.staticGroupName.Wrap(-1)
        self.bSizerGroupName.Add(self.staticGroupName, 0,
                            wx.ALIGN_CENTER | wx.ALL, 5)

        self.textGroupName = wx.TextCtrl(
            self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        self.bSizerGroupName.Add(self.textGroupName, 1,
                            wx.ALIGN_CENTER | wx.ALIGN_RIGHT | wx.ALL, 5)
        self.bSizerRight.Add(self.bSizerGroupName, 0, wx.EXPAND, 5)

        self.bSizerCount = wx.BoxSizer(wx.HORIZONTAL)

        self.staticMapCount = wx.StaticText(
            self, wx.ID_ANY, '0 maps selected', wx.DefaultPosition, wx.DefaultSize, 0)
        self.staticMapCount.Wrap(-1)
        self.bSizerCount.Add(self.staticMapCount, 0,
                        wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.bSizerCount.Add((0, 0), 1, wx.EXPAND, 5)

        self.buttonExpand = wx.Button(
            self, wx.ID_ANY, '+', wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT)
        self.bSizerCount.Add(self.buttonExpand, 0, wx.ALL, 5)

        self.buttonCollapse = wx.Button(
            self, wx.ID_ANY, '-', wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT)
        self.bSizerCount.Add(self.buttonCollapse, 0, wx.ALL, 5)

        self.bSizerRight.Add(self.bSizerCount, 0, wx.EXPAND, 5)

        self.treeMaps = CustomTree(
            self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TR_DEFAULT_STYLE, agwStyle=wx.TR_DEFAULT_STYLE | CT.TR_AUTO_CHECK_CHILD | CT.TR_AUTO_CHECK_PARENT)
        self.root = self.treeMaps.AddRoot('Map Selection')
        self.treeMaps.Expand(self.root)

        self.bSizerRight.Add(self.treeMaps, 1, wx.ALL | wx.EXPAND, 5)

        self.bSizerMain.Add(self.bSizerRight, 3, wx.EXPAND, 5)

        self.SetSizer(self.bSizerMain)
        self.Layout()

        self.Centre(wx.BOTH)

        self.enable_group(False)

        self.buttonExpand.Bind(wx.EVT_BUTTON, self.OnExpand)
        self.buttonCollapse.Bind(wx.EVT_BUTTON, self.OnCollapse)
        self.listboxGroup.Bind(wx.EVT_LISTBOX, self.OnSelect)
        self.buttonAdd.Bind(wx.EVT_BUTTON, self.OnAdd)
        self.buttonDelete.Bind(wx.EVT_BUTTON, self.OnDelete)
        self.buttonSave.Bind(wx.EVT_BUTTON, self.OnSave)
        self.buttonApply.Bind(wx.EVT_BUTTON, self.OnApply)
        self.treeMaps.Bind(CT.EVT_TREE_ITEM_CHECKED, self.OnChecked)
        self.treeMaps.Bind(CT.EVT_TREE_ITEM_COLLAPSED, self.OnRootCollapsed)
        self.treeMaps.Bind(CT.EVT_TREE_ITEM_RIGHT_CLICK, self.OnThumb)
        self.staticMapCount.Bind(wx.EVT_LEFT_DCLICK, self.OnVersion)

    def __del__(self):
        pass

    def OnExpand(self, event):
        self.treeMaps.ExpandAll()

    def OnCollapse(self, event):
        self.treeMaps.CollapseAll()
        for category in self.casual.get('categories'):
            self.treeMaps.Expand(category['item'])
        self.treeMaps.Expand(self.root)

    def OnSelect(self, event):
        self.update_maps()

    def OnAdd(self, event):
        name_index = 1
        while 'Group {}'.format(name_index) in self.selections:
            name_index += 1
        name = 'Group {}'.format(name_index)
        self.selections[name] = {'maps': []}
        self.listboxGroup.Append(name)
        self.enable_group(True)
        index = self.listboxGroup.FindString(name, True)
        self.listboxGroup.SetSelection(index)
        self.update_maps()

    def OnDelete(self, event):
        index = self.listboxGroup.GetSelection()
        if index == -1:
            return
        text = self.listboxGroup.GetString(index)
        self.selections.pop(text)
        self.listboxGroup.Clear()
        for sel in self.selections:
            self.listboxGroup.Append(sel)
        if self.listboxGroup.IsEmpty():
            self.textGroupName.SetValue('')
            self.treeMaps.SetMaps([])
            self.update_count()
            self.staticMapCount.SetLabel('0 maps selected')
            self.enable_group(False)
        else:
            count = self.listboxGroup.GetCount()
            if index < count:
                self.listboxGroup.SetSelection(index)
            else:
                self.listboxGroup.SetSelection(count - 1)
            self.update_maps()

    def OnSave(self, event):
        index = self.listboxGroup.GetSelection()
        if index == -1 and self.selections:
            tf2cm.error(self, 'Select a group to save!')
            return
        elif index == -1:
            new_cm = {'version': 1,'selections': self.selections}
            tf2cm.write_cm(new_cm)
            return
        old_name = self.listboxGroup.GetString(index)
        new_name = self.textGroupName.GetValue().strip()
        if not new_name:
            new_name = old_name
            self.textGroupName.SetValue(old_name)
        if new_name != old_name and new_name in self.selections:
            tf2cm.error(self, 'Duplicated group name!')
            return
        if old_name != new_name:
            self.selections[old_name]['maps'] = self.treeMaps.GetMaps()
            self.selections[new_name] = self.selections[old_name]
            self.selections.pop(old_name)
            self.listboxGroup.Clear()
            for sel in self.selections:
                self.listboxGroup.Append(sel)
            index = self.listboxGroup.FindString(new_name)
            self.listboxGroup.SetSelection(index)
            self.update_maps()
        else:
            self.selections[new_name]['maps'] = self.treeMaps.GetMaps()
        new_cm = {'version': 1,'selections': self.selections}
        tf2cm.write_cm(new_cm)

    def OnApply(self, event):
        path = os.path.join(self.tf, 'casual_criteria.vdf')
        stat = tf2cm.write_casual(
            path, self.treeMaps.GetMaps(), self.maps_data)
        if stat:
            dlg = wx.MessageDialog(self, 'Go back to TF2 and click "LOAD SAVED SETTINGS" button in Casual Mode.',
                                   'Map selection exported', wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()

    def OnChecked(self, event):
        self.update_count()

    def OnRootCollapsed(self, event):
        if self.root == event.GetItem():
            self.treeMaps.Expand(self.root)

    def OnThumb(self, event):
        game_map = self.treeMaps.GetPyData(event.GetItem())
        if game_map is None:
            return
        name = '{}.png'.format(game_map)
        path = os.path.join(self.app_path, r'data\images', name)
        if not os.path.isfile(path):
            return
        image = None
        try:
            image = wx.Bitmap(path, wx.BITMAP_TYPE_ANY)
        except:
            return
        if hasattr(self, 'bitmapThumb') and self.bitmapThumb is not None:
            self.bitmapThumb.Destroy()
            self.bitmapThumb = None
        self.bitmapThumb = wx.StaticBitmap(
            self, wx.ID_ANY, image, wx.DefaultPosition, (image.GetWidth(), image.GetHeight()), 0)
        self.bSizerRight.Add(self.bitmapThumb, 0, wx.ALL | wx.ALIGN_CENTER | wx.EXPAND, 5)
        self.bitmapThumb.Bind(wx.EVT_LEFT_DOWN, self.OnClickThumb)
        self.Layout()

    def OnClickThumb(self, event):
        if hasattr(self, 'bitmapThumb') and self.bitmapThumb is not None:
            self.bitmapThumb.Destroy()
            self.bitmapThumb = None
            self.Layout()

    def OnVersion(self, event):
        dlg = wx.MessageDialog(self, 'TF2 Casual Manager (TF2CM)\n\nVersion: {}\nAuthor: deluxghost'.format(
            self.app_version), 'About', wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def enable_group(self, check):
        self.buttonExpand.Enable(check)
        self.buttonCollapse.Enable(check)
        self.textGroupName.Enable(check)
        self.treeMaps.Enable(check)
        self.buttonDelete.Enable(check)
        self.buttonApply.Enable(check)

    def update_maps(self):
        if self.old_sel and self.old_sel in self.selections and self.treeMaps.IsEnabled():
            self.selections[self.old_sel]['maps'] = self.treeMaps.GetMaps()
        index = self.listboxGroup.GetSelection()
        if index == -1:
            self.textGroupName.SetValue('')
            self.treeMaps.SetMaps([])
            self.update_count()
            self.enable_group(False)
            return
        name = self.listboxGroup.GetString(index)
        maps = self.selections[name]['maps']
        self.textGroupName.SetValue(name)
        self.treeMaps.SetMaps(maps)
        self.update_count()
        self.old_sel = name

    def update_count(self):
        count = len(self.treeMaps.GetMaps())
        if count == 1:
            self.staticMapCount.SetLabel('1 map selected')
        else:
            self.staticMapCount.SetLabel('{} maps selected'.format(count))

    def load_cm(self):
        self.old_sel = ''
        selections = self.cm['selections']
        self.selections = selections
        for sel in selections:
            self.listboxGroup.Append(sel)
        if self.selections:
            self.enable_group(True)
            self.listboxGroup.SetSelection(0)
        self.update_maps()

    def load_map_struct(self):
        for i, category in enumerate(self.casual.get('categories')):
            category_t = self.treeMaps.AppendItem(
                self.root, category['name'], ct_type=1)
            self.casual['categories'][i]['item'] = category_t
            for j, mode in enumerate(category.get('modes')):
                mode_t = self.treeMaps.AppendItem(
                    category_t, mode['name'], ct_type=1)
                self.casual['categories'][i]['modes'][j]['item'] = mode_t
                for k, game_map in enumerate(mode.get('maps')):
                    map_t = self.treeMaps.AppendItem(
                        mode_t, game_map['name'], ct_type=1)
                    self.treeMaps.SetPyData(map_t, game_map['bsp'])
                    self.casual['categories'][i]['modes'][j]['maps'][k]['item'] = map_t
        for category in self.casual.get('categories'):
            self.treeMaps.Expand(category['item'])
        self.treeMaps.Expand(self.root)
