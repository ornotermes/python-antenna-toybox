#! /bin/env python3

from PyNEC import *
import numpy as np
import math

def find_index_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

def geometry(freq, length, segments, wire):
    nec = nec_context()
    geo = nec.get_geometry()

    center = np.array([0,0,0])
    half = np.array([length/2, 0, 0])

    pt1 = center - half
    pt2 = center + half

    exitation_segment = math.ceil(segments/2)

    wire_tag = 1
    #geometry data
    geo.wire(wire_tag, segments, pt1[0], pt1[1], pt1[2], pt2[0], pt2[1], pt2[2], wire/2, 1.0, 1.0)
    nec.geometry_complete(0)

    #control commands
    nec.ex_card(0, wire_tag, exitation_segment, 0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0) #exitation card, where RF is injected
    nec.fr_card(0, 1, freq/1e6, 0 ) #frequency card
    nec.rp_card(0, 19, 37, 1000, 0, 0, 0, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0) #radiation pattern card

    return nec

def get_z(nec):
    inp = nec.get_input_parameters(0)
    z = inp.get_impedance()[0]

    return z

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

C = 299792458 #speed of light

if (__name__ == '__main__'):
    wire_dia = 5e-3 #in meters
    freq = 145e6 #in MHz
    dipole_steps = 100 #How many iterations to test
    dipole_min_wl = 0.45
    dipole_max_wl = 0.5
    dipole_segments = 31 #should be an odd number

    freq_wl = C / freq
    dipole_wls = np.arange(dipole_min_wl, dipole_max_wl, (dipole_max_wl - dipole_min_wl) / dipole_steps) #Array of dipole wavelengths to test

    z = np.array([])
    for wl in dipole_wls:
        nec = geometry(freq, freq_wl * wl, dipole_segments, wire_dia)
        z = np.append(z, [get_z(nec)])
    
    for i in range(dipole_steps):
        print( f"{i : 5} \
| WL: {dipole_wls[i] : 2.03f} \
| L: {dipole_wls[i]*freq_wl : 2.03f} \
| R: {z.real[i] : 8.01f} \
| X: {z.imag[i] : 8.01f} \
| Z: {z_mag(z[i]) : 8.01f}\
| REF: {reflection(z[i], 50) : 8.02f}\
| VSWR: {vswr(z[i], 50) : 8.02f}\
" )

    i = find_index_nearest(z.imag, 0.0)
    print( "Most resonant: " )
    print( f"{i : 5} \
| WL: {dipole_wls[i] : 2.03f} \
| L: {dipole_wls[i]*freq_wl : 2.03f} \
| R: {z.real[i] : 8.01f} \
| X: {z.imag[i] : 8.01f} \
| Z: {z_mag(z[i]) : 8.01f}\
| REF: {reflection(z[i], 50) : 8.02f}\
| VSWR: {vswr(z[i], 50) : 8.02f}\
    " )