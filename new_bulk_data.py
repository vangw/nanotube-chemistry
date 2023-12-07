#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 14:29:13 2023

@author: spet5177
"""

import sys
import numpy as np
import os
import csv

# Length given in nm unless au stated then in Bohr radii
path = None
output_path = None
files = []

def main():
    try:
        if sys.argv[1] == "C":
            path = "/home/mw3/mw/spet5177/SWNT_xyz/CNT/"
            output_path = "/home/mw3/mw/spet5177/SWNT_xyz/CNT/data/"
        elif sys.argv[1] == "BN":
            path = "/home/mw3/mw/spet5177/SWNT_xyz/BNNT/"
            output_path = "/home/mw3/mw/spet5177/SWNT_xyz/BNNT/data/"
    except IndexError:
        print("Enter command line argument of C or BN")
    
    
    if path is None:
        print("No valid command line argument provided.")
    else:
        files = [file.name for file in os.scandir(path) if file.is_file()]
    for file in files:
        n, m = n_m_function(file)
        diameter, radius, length, unit_cell_length_au, unit_cell_atoms = prop_calc(n, m)
        recip_radius_squared = 1 / (radius**2)
        unit_cells, atoms, total_length, total_length_au = unit_calc(n, m)

        # Create a list for the current file's data
        data_for_current_file = [n, m, diameter, radius, recip_radius_squared, length, unit_cell_length_au, unit_cell_atoms, unit_cells, atoms, total_length, total_length_au]

        csv_filename = os.path.join(output_path, '{:}_{:}_data.csv'.format(n, m))
        
        # Open the CSV file and write the data
        with open(csv_filename, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['Variable Name', 'Value'])
            for var_name, var_value in zip(['n', 'm', 'diameter', 'radius', 'recip_radius_squared', 'length', 'unit_cell_length_au', 'unit_cell_atoms', 'unit_cells', 'atoms', 'total_length', 'total_length_au'], data_for_current_file):
                csv_writer.writerow([var_name, var_value])

def n_m_function(file):
    n,m = file[:-4].split("_")
    return int(n), int(m)


def dr_calc(x,y):
    gcd = lambda x,y : x if not y else gcd(y, x%y)
    d = gcd(x,y)
    if abs((x-y)) % (3 * d) == 0:
        dr = 3 * d
    else:
        dr = d
    return dr

def prop_calc(n,m):  
    dr = dr_calc(n, m)
    if sys.argv[1] == "C":
        r = 1.418 / 10
        
        circumference = (np.sqrt(3) * r * np.sqrt((n**2 + m**2 + n*m))) 
        diameter =  circumference / np.pi
        radius = diameter / 2
        length = (np.sqrt(3) * circumference)  / dr
        unit_cell_length_au = (length * 10) / 0.529177
        unit_cell_atoms = (4 * (n**2 + m**2 + n*m))/ dr
    elif sys.argv[1] == "BN":
        r = 1.446 / 10
        circumference = (np.sqrt(3) * r * np.sqrt((n**2 + m**2 + n*m)))
        diameter =  circumference / np.pi
        radius = diameter / 2
        length = (np.sqrt(3) * circumference)  / dr
        unit_cell_length_au = (length * 10) / 0.529177
        unit_cell_atoms = (4 * (n**2 + m**2 + n*m))/ dr
    else:
        print("Enter command line arguement of C or BN")
        pass
    return diameter, radius, length, unit_cell_length_au, unit_cell_atoms

def unit_calc(n,m):
    diameter, radius, length, unit_cell_length_au, unit_cell_atoms = prop_calc(n, m)
    if n == m or n == 0:
        unit_cells = 10
        atoms = unit_cell_atoms * unit_cells
    else:
        unit_cells = 1
        atoms = unit_cell_atoms * unit_cells
        while atoms <= 200:
            unit_cells += 1
            atoms = unit_cell_atoms * unit_cells
    total_length = length * unit_cells
    total_length_au = unit_cell_length_au * unit_cells
    return unit_cells, atoms, total_length, total_length_au

if __name__ == "__main__":
    main()
