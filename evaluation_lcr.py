import matplotlib.pyplot as plt
import numpy as np


# Messung_2022_12_14-15_11_47_Ersatzschaltung_LCR.txt
# Messung_2022_12_14-14_35 Quarzsand_LCR.txt


# Open the text file in read mode
with open(r"Messung_2022_12_14-15_11_47_Ersatzschaltung_LCR.txt", 'r') as file:
    # Move the file pointer to the desired position
    lines = file.readlines()
    
header_lines = []
data_lines = []

# Iterate over the lines of the file
for line in range(64):
    # Stores the header in header_lines
    header_lines.append(lines[line])
    
for line in range(65,len(lines)):
    # Stores the data in data_lines
    data_lines.append(lines[line])


data = []

# Iterate over the data lines
for line in data_lines:
    # Split the line by the delimiter and store the first four elements in the data list
    data.append(line.split('\t')[:4])

# Create a dictionary to store the data lists by first column value
data_by_first_column = {}

# Iterate over the data rows
for row in data:
    # Get the first column value of the current row
    first_column_value = row[0]
    
    # Check if the first column value is already a key in the dictionary
    if first_column_value in data_by_first_column:
        # If it is, append the current row to the existing list
        data_by_first_column[first_column_value].append(row)
    else:
        # If it isn't, create a new list in the dictionary with the current row as the first element
        data_by_first_column[first_column_value] = [row]


# Store each sweep in its own array
sweep_1 = data_by_first_column[list(data_by_first_column.keys())[0]]
sweep_2 = data_by_first_column[list(data_by_first_column.keys())[1]]
sweep_3 = data_by_first_column[list(data_by_first_column.keys())[2]]
sweep_4 = data_by_first_column[list(data_by_first_column.keys())[3]]
sweep_5 = data_by_first_column[list(data_by_first_column.keys())[4]]


# Define which sweep is evaluated
sweep_number = sweep_1

# Format the numbers from string to float so they can be plotted
for i in range(len(sweep_number)):
    for j in range(len(sweep_number[i])):
        sweep_number[i][j] = sweep_number[i][j].replace(',', '.')
        sweep_number[i][j] = float(sweep_number[i][j])
        


frequencies = []
magnitude = []
phase = []

# Store each column of the sweep in its own array
for row in sweep_number:
    frequencies.append(row[1])
    magnitude.append(row[2])
    phase.append(row[3])


# Create the plots
fig, ax = plt.subplots(2, 1, figsize=(8, 6))
plt.subplots_adjust(hspace=0.5)

ax[0].semilogx(frequencies, 20*np.log10(magnitude))
ax[0].set_xlabel('Frequency (Hz)')
ax[0].set_ylabel('Magnitude (dB)')
ax[0].grid(True)

ax[1].semilogx(frequencies, phase)
ax[1].set_xlabel('Frequency (Hz)')
ax[1].set_ylabel('Phase (rad)')
ax[1].grid(True)

plt.show()

