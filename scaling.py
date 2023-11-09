#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 14:53:32 2023

@author: spet5177
"""

import numpy as np
import sys

# Function to read XYZ file
def read_xyz(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    num_atoms = int(lines[0])
    atomic_symbols = []
    coordinates = []

    for line in lines[2:]:
        parts = line.split()
        atomic_symbols.append(parts[0])
        x, y, z = map(float, parts[1:4])
        coordinates.append([x, y, z])

    return num_atoms, atomic_symbols, coordinates

# Function to write XYZ file
def write_xyz(filename, atomic_symbols, coordinates):
    with open(filename, 'w') as f:
        f.write(f"{len(atomic_symbols)}\n")
        f.write("Scaled Carbon Nanotube\n")
        for symbol, (x, y, z) in zip(atomic_symbols, coordinates):
            f.write(f"{symbol} {x:.6f} {y:.6f} {z:.6f}\n")

# Read the XYZ file, need to select correct file to scale
# Eventually will automate this
input_xyz_file = "<path_to_filename>"
last_slash_index = input_xyz_file.rfind("/")
input_file_name = input_xyz_file[last_slash_index + 1:]
n,m = input_file_name.split("_")
m = m.split(".")[0]
print(n,m)
num_atoms, atomic_symbols, coordinates = read_xyz(input_xyz_file)


def scale(): 
    scaling_factor =  1 / 0.529177
    if sys.argv[1] == "C":
        output_xyz_file = "<path_to_folder/CNT_{:}_{:}.xyz".format(n, m)
    elif sys.argv[1] == "BN":
        output_xyz_file = "<path_to_folder/BNNT/BNNT_{:}_{:}.xyz".format(n, m)
    else:
        print("Please enter C or BN into command line")
    return scaling_factor, output_xyz_file


scaling_factor, output_xyz_file = scale()


# Scale the atomic coordinates
scaled_coordinates = np.array(coordinates) * scaling_factor

# Shift the coordiantes to far away point for computational ease
shifted_coordinates = scaled_coordinates + 50
print(shifted_coordinates)
# Write the modified coordinates to a new XYZ file
write_xyz(output_xyz_file, atomic_symbols, shifted_coordinates.tolist())

print(f"The nanotube has been scaled by a factor of {scaling_factor} and saved to {output_xyz_file}")
