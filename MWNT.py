#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 10:49:21 2023

@author: spet5177
"""

import numpy as np
import sys
import os

# In the command line input the size of the nanotubes require as "n1_m1 n2_m2"
innertube = "/home/mw3/mw/spet5177/SWNT_xyz/" + str(sys.argv[1]) + ".xyz"
outertube = "/home/mw3/mw/spet5177/SWNT_xyz/" + str(sys.argv[2]) + ".xyz"
print(innertube, outertube)

# Function to load XYZ data from a file
def load_tube(filename):
    with open(filename, "r") as file:
        lines = file.readlines()
        num_atoms = int(lines[0].strip())
        xyz_data = np.zeros((num_atoms, 3))
        for i, line in enumerate(lines[2:]):
            values = line.split()
            xyz_data[i] = [float(values[1]), float(values[2]), float(values[3])]
        return xyz_data
    
# Load XYZ data from the two nanotube files
nanotube1_xyz = load_tube(innertube)
nanotube2_xyz = load_tube(outertube)

# Calculate the offset to position the small nanotube inside the big nanotube
offset = np.array([0, 0, 0]) # Adjust this offset as needed

# Combine the XYZ coordinates
combined_xyz = np.vstack((nanotube1_xyz, nanotube2_xyz + offset))
output_file_name = "(" + str(sys.argv[1]) + ")" + "(" + str(sys.argv[2]) + ").xyz"
output_file_path = os.path.join("/home/mw3/mw/spet5177/MWNT_xyz/", output_file_name)
print(output_file_path)
# Write the combined XYZ coordinates to a new XYZ file
with open(output_file_path, "w") as output_file:
    output_file.write("{}\n\n".format(combined_xyz.shape[0]))
    for i in range(combined_xyz.shape[0]):
        output_file.write("C{} {:<10} {:<10} {:<10}\n".format(i + 1, combined_xyz[i, 0], combined_xyz[i, 1], combined_xyz[i, 2]))



# with open("nanotube_{:}_{:}.xyz".format(n, m), "w") as vmd:
#    vmd.write("{:}\n\n " .format(tube.shape[0]))
#    for i in range(tube.shape[0]):
#        vmd.write("C{:} {:<10} {:<10} {:<10}\n" .format(i+1, tube[i,0], tube[i,1], tube[i,2]))
        