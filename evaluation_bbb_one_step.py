import numpy as np
import matplotlib.pyplot as plt
import math
import os
import re

file_path = r"C:\Users\jonas\Desktop\m1\100 1000 k\step1.txt"

# Must be >= 1000
number_of_samples = 10000

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


# fig, ax = plt.subplots(2,2, figsize=(8,6))
# ax[0][0].plot(time_vector, voltage)
# ax[0][0].plot(time_vector, current)

# ax[0][1].semilogx(frequency_vector, magnitudes_voltage)
# ax[0][1].semilogx(frequency_vector, magnitudes_current)
    
# plt.show()



