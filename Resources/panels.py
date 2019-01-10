#!/usr/bin/env python
# encoding: utf-8
import wx, random
from .audio import Bell, audioServer

class BasePanel(wx.Panel):
    def __init__(self, parent, rang=None):
        wx.Panel.__init__(self, parent, -1, style=wx.SUNKEN_BORDER)
        self.Bind(wx.EVT_KEY_DOWN, self.onKeyDown)

    def onKeyDown(self, evt):
        key = evt.GetKeyCode()
        alt = evt.AltDown()
        if key in range(48, 58):
            rang = evt.GetKeyCode() - 48
            rang = (rang - 1) % 10
            if alt:
                rang += 10
            self.GetParent().GetParent().play(rang)

class GainPanel(BasePanel):
    def __init__(self, parent):
        BasePanel.__init__(self, parent)
        box = wx.BoxSizer(wx.HORIZONTAL)
        self.gainText = wx.StaticText(self, -1, label="Gain:")
        box.Add(self.gainText, 0, wx.ALIGN_CENTER_VERTICAL)
        self.gainSlider = wx.Slider(self, -1, minValue=0, maxValue=200, value=100)
        self.gainSlider.Bind(wx.EVT_SLIDER, self.setGain)
        self.gainSlider.Bind(wx.EVT_KEY_DOWN, self.onKeyDown)
        box.Add(self.gainSlider, 1, wx.EXPAND|wx.ALL, 5)

        self.detuneText = wx.StaticText(self, -1, label="Detune:")
        box.Add(self.detuneText, 0, wx.ALIGN_CENTER_VERTICAL)
        self.detuneSlider = wx.Slider(self, -1, minValue=0, maxValue=100, value=50)
        self.detuneSlider.Bind(wx.EVT_SLIDER, self.setDetune)
        self.detuneSlider.Bind(wx.EVT_KEY_DOWN, self.onKeyDown)
        box.Add(self.detuneSlider, 1, wx.EXPAND|wx.ALL, 5)

        self.SetSizer(box)

    def setGain(self, evt):
        audioServer.amp = evt.GetInt() * 0.01

    def setDetune(self, evt):
        detune = evt.GetInt() * 0.01
        for panel in self.GetParent().GetParent().bellPanels:
            panel.setDetune(detune)

class BellPanel(BasePanel):
    def __init__(self, parent, rang):
        BasePanel.__init__(self, parent, rang)
        self.bell = Bell(rang)
        freq = self.bell.waveguide.freq
        box = wx.BoxSizer(wx.VERTICAL)
        self.freqText = wx.StaticText(self, -1, label="%d" % freq)
        font, psize = self.freqText.GetFont(), self.freqText.GetFont().GetPointSize()
        font.SetPointSize(psize-2)
        self.freqText.SetFont(font)
        box.Add(self.freqText, 0, wx.LEFT, 2)
        self.freqSlider = wx.Slider(self, -1, minValue=20, maxValue=2000, value=freq,
                                    size=(-1,200), style=wx.SL_VERTICAL|wx.SL_INVERSE)
        self.freqSlider.Bind(wx.EVT_SLIDER, self.setFreq)
        self.freqSlider.Bind(wx.EVT_KEY_DOWN, self.onKeyDown)
        box.Add(self.freqSlider, 1, wx.EXPAND, 0)
        self.SetSizer(box)
    
    def playSound(self):
        self.bell.play()

    def setFreq(self, evt):
        freq = evt.GetInt()
        self.freqText.SetLabel("%d" % freq)
        self.bell.setFreq(freq)
    
    def setDetune(self, x):
        self.bell.setDetune(x)
