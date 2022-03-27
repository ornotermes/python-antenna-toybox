#! /bin/env python3

from PyNEC import *
import numpy as np
import math
import nec_helper as nh

def antenna(freq, length, segments, wire):
    n = nh.nec_helper()

    exitation_segment = math.ceil(segments/2)
    wire_tag = 1

    #geometry data
    n.wire_vertical(wire_tag, segments, length, 0, wire)
    n.geometry_complete()

    #control commands
    n.exitement(wire_tag, exitation_segment)
    n.frequency(freq, 1, 0)
    n.radiation_pattern()

    return n

if (__name__ == '__main__'):
    wire_dia = 5e-3 #in meters
    freq = 145e6 #in Hz
    dipole_steps = 100 #How many iterations to test
    dipole_min_wl = 0.45
    dipole_max_wl = 0.5
    dipole_segments = 31 #should be an odd number

    freq_wl = nh.wavelenth(freq)
    dipole_wls = np.arange(dipole_min_wl, dipole_max_wl, (dipole_max_wl - dipole_min_wl) / dipole_steps) #Array of dipole wavelengths to test

    z = np.array([])
    for wl in dipole_wls:
        n = antenna(freq, freq_wl * wl, dipole_segments, wire_dia)
        z = np.append(z, [n.get_imp(0)])
    
    for i in range(dipole_steps):
        print( f"{i : 5} \
| WL: {dipole_wls[i] : 2.03f} \
| L: {dipole_wls[i]*freq_wl : 2.03f} \
| R: {z.real[i] : 8.01f} \
| X: {z.imag[i] : 8.01f} \
| Z: {nh.z_mag(z[i]) : 8.01f}\
| REF: {nh.reflection(z[i], 50) : 8.02f}\
| VSWR: {nh.vswr(z[i], 50) : 8.02f}\
" )

    i = nh.find_index_nearest(z.imag, 0.0)
    print( "Most resonant: " )
    print( f"{i : 5} \
| WL: {dipole_wls[i] : 2.03f} \
| L: {dipole_wls[i]*freq_wl : 2.03f} \
| R: {z.real[i] : 8.01f} \
| X: {z.imag[i] : 8.01f} \
| Z: {nh.z_mag(z[i]) : 8.01f}\
| REF: {nh.reflection(z[i], 50) : 8.02f}\
| VSWR: {nh.vswr(z[i], 50) : 8.02f}\
    " )