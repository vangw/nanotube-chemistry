#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 09:33:30 2023

@author: spet5177
"""

import numpy as np

# Load the XYZ file into a NumPy array
xyz_data = np.loadtxt("<path_to_folder>" , skiprows=2, usecols=(1,2,3))

# Extract the coordinates of the first atom
first_atom_coordinates = xyz_data[0, :]

# Calculate distances between the first atom and all other atoms
distances = np.linalg.norm(xyz_data[1:, :] - first_atom_coordinates, axis=1)

# Find the minimum distance and its index
min_distance = np.min(distances)
min_distance_index = np.argmin(distances)

# Print the minimum distance and the index of the atom with the minimum distance
print(f"Minimum distance: {min_distance} (Angstroms)")
print(f"Index of the closest atom: {min_distance_index}")
