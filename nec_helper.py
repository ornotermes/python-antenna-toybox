from PyNEC import *
import numpy as np
import math

def z_mag(imp):
    return math.sqrt(imp.real**2+imp.imag**2)

def reflection(imp, ref):
    z = z_mag(imp)
    re = (z - ref) / (z + ref)
    return re

def vswr(imp, ref):
    r = reflection(imp, ref)
    vswr=(r+1)/(r-1)
    return vswr

def find_index_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

def wavelenth(freq):
    return C / freq

C = 299792458 #speed of light

class nec_helper():

    def __init__(self):
        self.nec = nec_context()
        self.geo = self.nec.get_geometry()

    def wire_vertical( self, tag, segments, length, position, diameter ):
        center = np.array([position, 0, 0])
        half = np.array([position, length/2, 0])

        p1 = center - half
        p2 = center + half

        self.geo.wire( tag, segments, p1[0], p1[1], p1[2], p2[0], p2[1], p2[2], diameter/2, 1.0, 1.0)

    def geometry_complete(self):
        self.nec.geometry_complete(0)

    def exitement(self, tag, segment):
        self.nec.ex_card(0, tag, segment, 0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0) #exitation card, where RF is injected

    def frequency(self, start, steps, increment):
        self.nec.fr_card(0, steps, start/1e6, increment ) #frequency card
    
    def radiation_pattern(self):
        self.nec.rp_card(0, 19, 37, 1000, 0, 0, 0, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0) #radiation pattern card

    def get_imp(self,index):
        inp = self.nec.get_input_parameters(index)
        z = inp.get_impedance()[0]
        return z