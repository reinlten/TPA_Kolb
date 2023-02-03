import numpy as np
import matplotlib.pyplot as plt
import math
import os
import re

def messschritt(file_path, amplitudes, phases, frequencies):
    with open(file_path, "r") as file:
        lines = file.readlines()
    
    file.close()

    number_of_samples = 10000 
    

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
        data.append(line.split(' '))

    header_lines = header_lines[0].strip() # remove the newline character
    values = header_lines.split(" ") # split the string into a list of strings
    current_freq = int(values[0])
    sample_freq = int(values[1])
    number_of_periods = int(values[2])
    number_of_samples_per_period = int(values[3])

    for i in range(len(data)):
        data[i][1] = data[i][1].rstrip()
        
    dt = 1 / sample_freq
    df = sample_freq /number_of_samples
    time_vector = np.arange(0, number_of_samples * dt, dt)
    frequency_vector = np.arange(0, sample_freq, df)
        
    frequencies.append(current_freq)
        
    voltage = []
    current = []

    # Stores each signal in its own array
    for row in data:
        voltage.append(row[0])
        current.append(row[1])

    # Perform the FFT on the signal
    fft_coefficients_voltage = np.fft.fft(voltage, norm="forward")
    fft_coefficients_current = np.fft.fft(current, norm="forward")

    # Calculate the amplitudes of the signal
    amplitudes_voltage = np.abs(fft_coefficients_voltage)
    amplitudes_current = np.abs(fft_coefficients_current)

    # Calculate the phases of the signal
    phases_voltage = np.angle(fft_coefficients_voltage)
    phases_current = np.angle(fft_coefficients_current)

    # real1 = amplitudes_voltage * np.cos(phases_voltage)
    # imag1 = amplitudes_current * np.sin(phases_current)

    # real2 = [x.real for x in fft_coefficients_current]
    # imag2 = [x.imag for x in fft_coefficients_current]

    # plt.plot(real1, imag1)
    # plt.plot(real2, imag2)
    # plt.show()

    # fig, ax = plt.subplots(2, 2, figsize=(10, 8))
    # plt.subplots_adjust(hspace=0.3, wspace=0.5)

    # ax[0][0].semilogx(frequency_vector, 20*np.log10(amplitudes1))
    # ax[0][0].semilogx(frequency_vector, 20*np.log10(amplitudes2))
    # ax[0][0].set_xlabel('Frequency (Hz)')
    # ax[0][0].set_ylabel('Magnitude (dB)')
    # ax[0][0].grid(True)

    # ax[0][1].plot(frequency_vector, amplitudes1)
    # ax[0][1].plot(frequency_vector, amplitudes2)
    # ax[0][1].set_xlabel('Frequency (Hz)')
    # ax[0][1].set_ylabel('Magnitude (mv)')
    # ax[0][1].grid(True)

    # ax[1][0].semilogx(frequency_vector, phases2 - phases1)
    # ax[1][0].set_xlabel('Frequency (Hz)')
    # ax[1][0].set_ylabel('Phase (rad)')
    # ax[1][0].grid(True)

    # ax[1][1].plot(frequency_vector, phases2 - phases1)
    # ax[1][1].set_xlabel("Realteil")
    # ax[1][1].set_ylabel("Imaginärteil")
    # plt.show()

    index = current_freq // 1000
    print(f"index: {index}")
    print(frequency_vector[index])

    print(f"Amplitude of voltage: {amplitudes_voltage[index]}")
    print(f"Amplitude of current: {amplitudes_current[index]}")
    print(f"Phase of voltage: {phases_voltage[index]}")
    print(f"Phase of current: {phases_current[index]}")


    # plt.semilogx(frequency_vector, dif)
    # plt.semilogx(frequency_vector, diff)

    # plt.show()
    
    amplitude = amplitudes_voltage[index] / (amplitudes_current[index] / 100)
    phase = (360 / (2*math.pi)) * (phases_voltage[index] - phases_current[index])
    print(f"The current amplitude is: {amplitude} Ohm")
    print(f"The current phase is: {phase} degrees")

    # plt.plot(time_vector, signal_1 - amplitudes1[0], label="signal 1")
    # plt.plot(time_vector, signal_2 - amplitudes2[0], label="signal2")
    # plt.legend()
    # plt.show()


    diff_amplitude = amplitude / 369 * 100
    diff_phase = phase / -18.6 * 100

    print(diff_amplitude, diff_phase)
    amplitudes.append(amplitude)
    phases.append(phase)

def messbereich(range_path, amplitudes, phases, frequencies):
    file_paths = os.listdir(range_path)
    file_paths = sorted(file_paths, key=extract_number)

    for file in file_paths:
       file_path = os.path.join(range_path, file)
       messschritt(file_path, amplitudes, phases, frequencies)
       
def messung(measurement_path):
    amplitudes = []
    phases = []
    frequencies = []
    
    folder_paths = os.listdir(measurement_path)
    folder_paths = sorted(folder_paths, key=extract_number)

    for folder in folder_paths:
        folder_path = os.path.join(measurement_path, folder)
        messbereich(folder_path, amplitudes, phases, frequencies)
    
    return amplitudes, phases, frequencies

def extract_number(file_path):
    match = re.search(r'\d+', file_path)
    if match:
        return int(match.group(0))
    return 0

def plot(amplitudes, phases, frequencies):
    fig, ax = plt.subplots(2, 1, figsize=(8, 6))
    plt.subplots_adjust(hspace=0.5)

    ax[0].semilogx(frequencies, amplitudes)
    ax[0].set_xlabel('Frequency (Hz)')
    ax[0].set_ylabel("Magnitude (Ohm)")
    
    ax[1].semilogx(frequencies, phases)
    ax[1].set_xlabel('Frequency (Hz)')
    ax[1].set_ylabel("Phase (°)")
    
    plt.show()
    
def main():
    measurement_path = r"C:\Users\jonas\Desktop\Uni\Teamprojektarbeit\Aktuell\Messungen BBB\14.12.2022_AP_1"
    
    amplitudes, phases, frequencies = messung(measurement_path)
    plot(amplitudes, phases, frequencies)
    
if __name__ == '__main__':
    main()



