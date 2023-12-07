import os
import pandas as pd

output_data_path = "/u/mw/spet5177/data/CNT/armchair"
input_data_path = "/u/mw/spet5177/SWNT_xyz/CNT/data"
output_csv_path = "/u/mw/spet5177/output_data.csv"

# Function to extract potential and kinetic energy from the eng1.out file
def extract_energy(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
        potential_energy = float(lines[-1].split()[1])
        kinetic_energy = float(lines[-1].split()[2])
    return potential_energy, kinetic_energy

# Create an empty DataFrame to store the data
output_data_df = pd.DataFrame()

# Iterate through the folders in the output data path
for folder_name in os.listdir(output_data_path):
    folder_path = os.path.join(output_data_path, folder_name)

    # Check if the item is a directory
    if os.path.isdir(folder_path):
        # Extract n and m from the folder name
        n, m = map(int, folder_name.split('_'))

        # Construct the corresponding input data file name
        input_data_file = f"{n}_{m}_data.csv"
        input_data_file_path = os.path.join(input_data_path, input_data_file)

        # Check if the input data file exists
        if os.path.isfile(input_data_file_path):
            # Read the input data file
            input_data_df = pd.read_csv(input_data_file_path)

            # Extract potential and kinetic energy from eng1.out
            eng_file_path = os.path.join(folder_path, "eng1.out")
            potential_energy, kinetic_energy = extract_energy(eng_file_path)

            # Add potential and kinetic energy to the input data DataFrame
            input_data_df['Potential Energy'] = potential_energy
            input_data_df['Kinetic Energy'] = kinetic_energy

            # Append the data to the output DataFrame
            output_data_df = output_data_df.append(input_data_df, ignore_index=True)

# Save the combined data to a CSV file
output_data_df.to_csv(output_csv_path, index=False)

print(f"Data has been successfully combined and saved to {output_csv_path}")
