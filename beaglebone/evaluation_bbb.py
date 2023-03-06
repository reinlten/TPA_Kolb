import numpy as np
import matplotlib.pyplot as plt
import math
import os
import re

measurement_path = r"C:\Users\jonas\Desktop\Uni\Teamprojektarbeit\Aktuell\Messungen BBB\14.12.2022_AP_1"

number_of_samples = 100000

magnitudes = []
phases = []
frequencies = []

def extract_number(file_path):
    match = re.search(r'\d+', file_path)
    if match:
        return int(match.group(0))
    return 0

folder_paths = os.listdir(measurement_path)
folder_paths = sorted(folder_paths, key=extract_number)

for folder in folder_paths:
    folder_path = os.path.join(measurement_path, folder)
    file_paths = os.listdir(folder_path)
    file_paths = sorted(file_paths, key=extract_number)

    for file in file_paths:
        file_path = os.path.join(folder_path, file)
        
        number_of_samples = 100000

        with open(file_path, "r") as file:
            lines = file.readlines()

        file.close()

        header_lines = []
        data_lines = []

        # Iterate over the lines of the file
        for line in range(1):
            # Stores the header in header_lines
            header_lines.append(lines[line])
            
        for line in range(1,number_of_samples + 1):
            # Stores the data in data_lines
            data_lines.append(lines[line])


        data = []
        header = []

        for line in data_lines:
            data.append(line.split())


        header_lines = header_lines[0].strip()
        values = header_lines.split(" ")
        current_freq = int(values[0])
        sample_freq = int(values[1])
        number_of_periods = int(values[2])
        number_of_samples_per_period = int(values[3])

        for i in range(len(data)):
            data[i][1] = data[i][1].rstrip()
            data[i][0] = int(data[i][0])
            data[i][1] = int(data[i][1])
            
        dt = 1 / sample_freq
        df = sample_freq /number_of_samples
        time_vector = np.arange(0, number_of_samples * dt, dt)
        frequency_vector = np.arange(0, sample_freq, df)
            
        voltage = []
        current = []

        # Stores each signal in its own array
        for row in data:
            voltage.append(row[0])
            current.append(row[1])

        # Perform the FFT on the signal
        fft_coefficients_voltage = np.fft.fft(voltage)
        fft_coefficients_current = np.fft.fft(current)

        real__part_of_voltage = np.real(fft_coefficients_voltage)
        real__part_of_current = np.real(fft_coefficients_current)

        imag_part_of_voltage = np.imag(fft_coefficients_voltage)
        imag_part_of_current = np.imag(fft_coefficients_current)

        # Calculate the amplitudes of the signal
        magnitudes_voltage = 2 * np.abs(fft_coefficients_voltage) / number_of_samples
        magnitudes_current = 2 * np.abs(fft_coefficients_current) / number_of_samples

        # Calculate the phases of the signal
        phases_voltage = np.angle(fft_coefficients_voltage)
        phases_current = np.angle(fft_coefficients_current)

        index = np.where(frequency_vector == current_freq)
        index = index[0][0]


        print(f"Magnitude of voltage: {magnitudes_voltage[index]} Volt")
        print(f"Magnitude of current: {magnitudes_current[index]} Ampere")
        print(f"Phase of voltage: {phases_voltage[index]} rad")
        print(f"Phase of current: {phases_current[index]} rad")

        magnitude = magnitudes_voltage[index] / magnitudes_current[index]
        phase = (360 / (2*math.pi)) * (phases_voltage[index] - phases_current[index])

        print(f"Magnitude of Impedance: {magnitude} Ohm")
        print(f"Phase of Impedance: {phase} degrees")

        frequencies.append(current_freq)
        magnitudes.append(magnitude)
        phases.append(phase)
        

fig, ax = plt.subplots(2, 1, figsize=(8, 6))
plt.subplots_adjust(hspace=0.5)

ax[0].semilogx(frequencies, magnitudes)
ax[0].set_xlabel('Frequency (Hz)')
ax[0].set_ylabel("Magnitude (Ohm)")

ax[1].semilogx(frequencies, phases)
ax[1].set_xlabel('Frequency (Hz)')
ax[1].set_ylabel("Phase (°)")

plt.show()