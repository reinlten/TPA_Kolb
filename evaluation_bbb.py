import numpy as np
import matplotlib.pyplot as plt
import math
import os
import re

measurement_path = r"C:\Users\jonas\Desktop\Teamprojektarbeit\Aktuell\Messungen BBB\07.02.2023_1"

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

        header = lines[0]
        data = lines[1:]
        
        current_freq, sample_freq, number_of_periods, number_of_samples_per_period = header.split()
        
        current_freq = int(current_freq)
        sample_freq = int(sample_freq)
        number_of_periods = int(number_of_periods)
        number_of_samples_per_period = int(number_of_samples_per_period)
        
        number_of_samples = 10 * (sample_freq // current_freq)
        
        voltage1 = []
        voltage2 = []
    

        for i in range(number_of_samples):
                first, second = data[i].split()
                voltage1.append(int(first))
                voltage2.append(int(second))
       
        factor = 4700 / (max(voltage1) / 2)

        for i in range(len(voltage1)):
            voltage1[i] *= factor
        
        print(f"Factor: {factor}")

        dt = 1 / sample_freq
        df = sample_freq / number_of_samples
        time_vector = np.arange(0, number_of_samples * dt, dt)
        frequency_vector = np.arange(0, number_of_samples * df, df)
        
        fft_coefficients_voltage1 = 2 * np.fft.fft(voltage1) / number_of_samples
        fft_coefficients_voltage2 = 2 * np.fft.fft(voltage2) / number_of_samples

        fft_coefficients_voltage1[0] /= 2
        fft_coefficients_voltage2[0] /= 2
        
        fft_coefficients_voltage_dut = []
        for i in range(len(fft_coefficients_voltage1)):
            fft_coefficients_voltage_dut.append(fft_coefficients_voltage1[i] - fft_coefficients_voltage2[i])

        current = list(map(lambda x: x / 100, voltage2))
        
        fft_coefficients_current = 2 * np.fft.fft(current) / number_of_samples
        
        fft_coefficients_current[0] /= 2
        
        magnitudes_voltage_dut = np.abs(fft_coefficients_voltage_dut)
        magnitudes_current = np.abs(fft_coefficients_current)

        # Berechnet die Phases der DUT-Spannung und dem DUT-Strom
        phases_voltage_dut = np.angle(fft_coefficients_voltage_dut)
        phases_current = np.angle(fft_coefficients_current) 

        print(f"Current frequency: {current_freq}")

        print(f"Magnitude of DC component of voltage: {magnitudes_voltage_dut[0]} mV")
        print(f"Magnitude of DC component of current: {magnitudes_current[0]} mA")

        index = int(current_freq / df)

        phase_voltage_dut = (360 / (2*math.pi)) * phases_voltage_dut[index]
        phase_current = (360 / (2*math.pi)) * phases_current[index]

        print(f"Magnitude of voltage: {magnitudes_voltage_dut[index]} mV")
        print(f"Magnitude of current: {magnitudes_current[index]} mA")
        print(f"Phase of voltage: {phase_voltage_dut} degrees")
        print(f"Phase of current: {phase_current} degrees")

        # Berechnet die Amplitude und die Phase der Impedanz bei der aktuellen Frequenz
        magnitude_impedance_dut = magnitudes_voltage_dut[index] / magnitudes_current[index]
        phase_impedance_dut = phase_voltage_dut - phase_current

        print(f"Magnitude of Impedance: {magnitude_impedance_dut} Ohm")
        print(f"Phase of Impedance: {phase_impedance_dut} degrees")

        # plt.plot(frequency_vector, magnitudes_voltage_dut)
        # plt.plot(frequency_vector, magnitudes_current)
        # plt.xlim(0,current_freq*2)
        # plt.show()

        frequencies.append(current_freq)
        magnitudes.append(magnitude_impedance_dut)
        phases.append(phase_impedance_dut)
        
fig, ax = plt.subplots(2, 1, figsize=(8, 6))
plt.subplots_adjust(hspace=0.5)

ax[0].semilogx(frequencies, magnitudes)
ax[0].set_xlabel('Frequency (Hz)')
ax[0].set_ylabel("Magnitude (Ohm)")

ax[1].semilogx(frequencies, phases)
ax[1].set_xlabel('Frequency (Hz)')
ax[1].set_ylabel("Phase (°)")

plt.show()