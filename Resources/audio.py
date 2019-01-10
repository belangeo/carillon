#!/usr/bin/env python
# encoding: utf-8
"""
Definition du materiel audio.

"""
from pyo import *
from .config import *

audioServer = Server(sr=44100, nchnls=2, buffersize=256).boot()
audioServer.start()

frequencies = midiToHz(MIDI_NOTES)
bnoise = Noise()
envelope = CosTable([(0,0), (25,1), (500,0),(8192,0)])

class Bell:
    def __init__(self, rang):
        self.trig = Trig().stop()
        self.amp = TrigEnv(self.trig, table=envelope, dur=.2)
        self.excite = Tone(bnoise * self.amp, freq=3000, mul=1)
        self.denorm = Denorm(self.excite)
        self.waveguide = AllpassWG(self.denorm, freq=frequencies[rang], feed=.9999, mul=.3)
        self.hpfilter = Biquadx(self.waveguide, freq=frequencies[rang], q=2, type=1, stages=2)
        self.pan = SPan(self.hpfilter, pan=rang/(NUM_OF_BELLS-1.0)).out()
    
    def play(self):
        self.trig.play()

    def setFreq(self, x):
        self.waveguide.freq = x
        self.hpfilter.freq = x
        
    def setDetune(self, x):
        self.waveguide.detune = x
        
if __name__ == "__main__":
    b = Bell(0)
    audioServer.gui(locals())