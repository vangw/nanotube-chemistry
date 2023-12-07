import sys
import numpy as np
import os

path = None
output_path = None
files = []

def main():
    try:
        if sys.argv[1] == "C":
            global path
            path = "/home/mw3/mw/spet5177/SWNT_xyz/CNT/"

        elif sys.argv[1] == "BN":
            path = "/home/mw3/mw/spet5177/SWNT_xyz/BNNT/"

    except IndexError:
        print("Enter command line argument of C or BN")

    if path is None:
        print("No valid command line argument provided.")
    else:
        files = [file.name for file in os.scandir(path) if file.is_file()]
    for file in files:
        n, m = n_m_function(file)
        num_atoms, coordinates = read_xyz(file)
        scaling_factor, output_xyz_file = scale(n, m, num_atoms)
        # Scale the atomic coordinates
        scaled_coordinates = np.array(coordinates) * scaling_factor
        # Shift the coordiantes to far away point for computational ease
        shifted_coordinates = np.copy(scaled_coordinates)
        shifted_coordinates[:,0] += 50
        shifted_coordinates[:,1] += 50
        # Sort the coordinates based on the first character (B or N)
        sorted_coordinates = sorted(shifted_coordinates.tolist(), key=lambda x: x[0])
        # Write the sorted coordinates to the output file
        write_xyz(output_xyz_file, sorted_coordinates)

def n_m_function(file):
    n,m = file[:-4].split("_")
    return int(n), int(m)

# Function to read XYZ file
def read_xyz(file):
    with open(path+file, 'r') as f:
        lines = f.readlines()
        num_atoms = int(lines[0])
        atomic_symbols = []
        coordinates = []
    
    for line in lines[2:]:
        parts = line.split()
        atomic_symbols.append(parts[0])
        x, y, z = map(float, parts[1:4])
        coordinates.append([x, y, z])

    return num_atoms, coordinates

# Function to write XYZ file with correct formatting for Molecular Dynamics Code
def write_xyz(file, coordinates):
    with open(file, 'w') as f:
        f.write("T\n")
        f.write("F\n")
        f.write("F\n")
        f.write("F\n")
        f.write("F\n")
        for x, y, z in coordinates:
            f.write(f"{x:.6f} {y:.6f} {z:.6f}\n")

def scale(n, m, num_atoms):
    scaling_factor =  1 / 0.529177
    common_path = "/home/mw3/mw/spet5177/SWNT_xyz/"
    if sys.argv[1] == "C":
        output_xyz_file = common_path + "CNT/scaled/CNT_{:}_{:}_{:}.xyz".format(n, m, num_atoms)
    elif sys.argv[1] == "BN":
        output_xyz_file = common_path + "BNNT/scaled/BNNT_{:}_{:}_{:}.xyz".format(n, m, num_atoms)
    else:
        print("Please enter C or BN into command line")
        pass
    return scaling_factor, output_xyz_file

if __name__ == "__main__":
    main()
