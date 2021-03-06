#!/usr/bin/env python
# encoding: utf-8
"""
Simulation d'un jeu de gongs.

"""
import wx
from Resources.panels import GainPanel, BellPanel
from Resources.config import *

class MainFrame(wx.Frame):
    def __init__(self, parent, title, size):
        wx.Frame.__init__(self, parent, -1, title=title, size=size)
        self.mainPanel = wx.Panel(self)
        mainBox = wx.BoxSizer(wx.VERTICAL)
        bellBox = wx.BoxSizer(wx.HORIZONTAL)
        
        gainPanel = GainPanel(self.mainPanel)
        mainBox.Add(gainPanel, 0, wx.EXPAND)

        self.bellPanels = []
        for i in range(NUM_OF_BELLS):
            panel = BellPanel(self.mainPanel, i)
            self.bellPanels.append(panel)
            bellBox.Add(panel, 0, wx.EXPAND|wx.ALL, 2)
        panel.SetFocus()

        mainBox.Add(bellBox, 1, wx.EXPAND)
        self.mainPanel.SetSizer(mainBox)

    def play(self, rang):
        if rang < len(self.bellPanels):
            self.bellPanels[rang].playSound()
       
if __name__ == "__main__":
    app = wx.App(False)
    mainFrame = MainFrame(None, title='Carillon', size=(40*NUM_OF_BELLS+5, 300))
    mainFrame.Show()
    app.MainLoop()
