# -*- coding: utf-8 -*-

import wx
import wx.xrc
import wx.lib.agw.customtreectrl as CT


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

    def GetCheckedItems(self, itemParent=None, checkedItems=None):
        if itemParent is None:
            itemParent = self.GetRootItem()
        if checkedItems is None:
            checkedItems = []
        child, cookie = self.GetFirstChild(itemParent)
        while child:
            if self.IsItemChecked(child):
                checkedItems.append(child)
            checkedItems = self.GetCheckedItems(child, checkedItems)
            child, cookie = self.GetNextChild(itemParent, cookie)
        return checkedItems

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
        items = [i for i in self.GetAllItems() if self.GetPyData(i) is not None]
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

        bSizerMain = wx.BoxSizer(wx.HORIZONTAL)

        bSizerLeft = wx.BoxSizer(wx.VERTICAL)

        self.staticGroups = wx.StaticText(
            self, wx.ID_ANY, 'Map Groups:', wx.DefaultPosition, wx.DefaultSize, 0)
        self.staticGroups.Wrap(-1)
        bSizerLeft.Add(self.staticGroups, 0, wx.ALL | wx.EXPAND, 5)

        listboxGroupChoices = []
        self.listboxGroup = wx.ListBox(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                       listboxGroupChoices, wx.LB_NEEDED_SB | wx.LB_SINGLE | wx.LB_SORT)
        bSizerLeft.Add(self.listboxGroup, 1, wx.ALIGN_TOP |
                       wx.ALL | wx.EXPAND, 5)

        gSizerButtons = wx.GridSizer(2, 2, 0, 0)

        self.buttonAdd = wx.Button(
            self, wx.ID_ANY, 'Add', wx.DefaultPosition, wx.DefaultSize, 0)
        gSizerButtons.Add(self.buttonAdd, 0, wx.ALIGN_CENTER |
                          wx.ALL | wx.EXPAND, 5)

        self.buttonDelete = wx.Button(
            self, wx.ID_ANY, 'Delete', wx.DefaultPosition, wx.DefaultSize, 0)
        gSizerButtons.Add(self.buttonDelete, 0,
                          wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 5)

        self.buttonSave = wx.Button(
            self, wx.ID_ANY, 'Save', wx.DefaultPosition, wx.DefaultSize, 0)
        gSizerButtons.Add(self.buttonSave, 1,
                          wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 5)

        self.buttonApply = wx.Button(
            self, wx.ID_ANY, 'Apply', wx.DefaultPosition, wx.DefaultSize, 0)
        gSizerButtons.Add(self.buttonApply, 0,
                          wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 5)

        bSizerLeft.Add(gSizerButtons, 0, wx.ALIGN_BOTTOM |
                       wx.EXPAND | wx.RESERVE_SPACE_EVEN_IF_HIDDEN, 5)

        bSizerMain.Add(bSizerLeft, 1, wx.EXPAND, 5)

        bSizerRight = wx.BoxSizer(wx.VERTICAL)

        bSizerGroupName = wx.BoxSizer(wx.HORIZONTAL)

        self.staticGroupName = wx.StaticText(
            self, wx.ID_ANY, 'Group:', wx.DefaultPosition, wx.DefaultSize, 0)
        self.staticGroupName.Wrap(-1)
        bSizerGroupName.Add(self.staticGroupName, 0,
                            wx.ALIGN_CENTER | wx.ALL, 5)

        self.textGroupName = wx.TextCtrl(
            self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        bSizerGroupName.Add(self.textGroupName, 1,
                            wx.ALIGN_CENTER | wx.ALIGN_RIGHT | wx.ALL, 5)

        bSizerRight.Add(bSizerGroupName, 0, wx.EXPAND, 5)

        self.treeMaps = CustomTree(
            self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TR_DEFAULT_STYLE, agwStyle=wx.TR_DEFAULT_STYLE|CT.TR_AUTO_CHECK_CHILD|CT.TR_AUTO_CHECK_PARENT)
        self.root = self.treeMaps.AddRoot('Map Selection')
        self.treeMaps.Expand(self.root)

        bSizerRight.Add(self.treeMaps, 1, wx.ALL | wx.EXPAND, 5)

        bSizerMain.Add(bSizerRight, 3, wx.EXPAND |
                       wx.RESERVE_SPACE_EVEN_IF_HIDDEN, 5)

        self.SetSizer(bSizerMain)
        self.Layout()

        self.Centre(wx.BOTH)

        self.buttonAdd.Bind(wx.EVT_BUTTON, self.buttonAddOnButtonClick)
        self.buttonDelete.Bind(wx.EVT_BUTTON, self.buttonDeleteOnButtonClick)
        self.buttonSave.Bind(wx.EVT_BUTTON, self.buttonSaveOnButtonClick)
        self.buttonApply.Bind(wx.EVT_BUTTON, self.buttonApplyOnButtonClick)

    def __del__(self):
        pass

    def buttonAddOnButtonClick(self, event):
        pass

    def buttonDeleteOnButtonClick(self, event):
        pass

    def buttonSaveOnButtonClick(self, event):
        pass

    def buttonApplyOnButtonClick(self, event):
        pass

    def load_map_struct(self):
        for i, category in enumerate(self.casual.get('categories')):
            category_t = self.treeMaps.AppendItem(self.root, category['name'], ct_type=1)
            self.casual['categories'][i]['item'] = category_t
            for j, mode in enumerate(category.get('modes')):
                mode_t = self.treeMaps.AppendItem(category_t, mode['name'], ct_type=1)
                self.casual['categories'][i]['modes'][j]['item'] = mode_t
                for k, game_map in enumerate(mode.get('maps')):
                    map_t = self.treeMaps.AppendItem(mode_t, game_map['name'], ct_type=1)
                    self.treeMaps.SetPyData(map_t, game_map['bsp'])
                    self.casual['categories'][i]['modes'][j]['maps'][k]['item'] = map_t
        for category in self.casual.get('categories'):
            self.treeMaps.Expand(category['item'])
        self.treeMaps.Expand(self.root)
