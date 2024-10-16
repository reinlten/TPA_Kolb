import numpy as np
import matplotlib.pyplot as plt
import os
import re
import math


# Pfad wo die Ordner mit den Messungen liegen
measurement_path = r"C:\Users\jonas\Desktop\Teamprojektarbeit\Aktuell\Messungen BBB\15.09.2023\5"
shunt_value = 12000

# Arrays für die Speicherung der Amplituden, Phasen und Frequenzen
magnitudes = []
phases = []
frequencies = []
real_parts = []
imag_parts = []
last_phase = 0
spannungsverhältnis = []

# Hilfsfunktion zur Sortierung der Dateien
def extract_number(file_path):
    match = re.search(r'\d+', file_path)
    if match:
        return int(match.group(0))
    return 0

file_paths = os.listdir(measurement_path)
file_paths = sorted(file_paths, key=extract_number)

# Ab hier Auswertung einer Textdatei
for file in file_paths:
    file_path = os.path.join(measurement_path, file)
    
    # Textdatei wird gelesen
    with open(file_path, "r") as file:
        lines = file.readlines()

    file.close()

    # Header und Daten werden geteilt
    header = lines[0]
    data = lines[1:]
    
    # Header wird ausgelesen und gespeichert
    current_freq, sample_freq, number_of_periods, number_of_samples_per_period = header.split()
    
    # Headerwerte werden in die richtige Form gebracht
    current_freq = int(current_freq)
    sample_freq = int(sample_freq)
    number_of_periods = int(number_of_periods)
    number_of_samples_per_period = int(number_of_samples_per_period)
    
    # Datenwerte werden in Gesamtspannung (voltage1) und Shuntspannung (voltage2) geteilt
    voltage1 = []
    voltage2 = []
    
    number_of_samples = len(data)
    
    for i in range(number_of_samples):
            first, second = data[i].split()
            voltage1.append(int(first))
            voltage2.append(int(second))
    
    # proportiontocut = 0.05  # Proportion of values to cut
    # voltage1 = stats.mstats.winsorize(voltage1, limits=[proportiontocut, proportiontocut])
    # voltage2 = stats.mstats.winsorize(voltage2, limits=[proportiontocut, proportiontocut])

    # Größen for die Visualisierung werden berechnet
    dt = 1 / sample_freq
    df = sample_freq / number_of_samples
    time_vector = np.arange(0, number_of_samples * dt, dt)
    frequency_vector = np.arange(0, number_of_samples * df, df)
    
    # Fourierkoeffizienten der beiden Spannungen werden berechnet 
    fft_coefficients_voltage1 = 2 * np.fft.fft(voltage1) / number_of_samples
    fft_coefficients_voltage2 = 2 * np.fft.fft(voltage2) / number_of_samples

    fft_coefficients_voltage1[0] /= 2
    fft_coefficients_voltage2[0] /= 2

    
    # Fourierkoeffizienten der DUT-Spannung wird berechnet
    fft_coefficients_voltage_dut = []
    for i in range(len(fft_coefficients_voltage1)):
        fft_coefficients_voltage_dut.append(fft_coefficients_voltage1[i] - fft_coefficients_voltage2[i])
  
    # Stromstärkewerte durch DUT werden über Ohmsches Gesetz und Shuntspannung berechnet
    current = list(map(lambda x: x / shunt_value, voltage2))

    # Fourrierkoeffizienten des Stroms werden berechnet
    fft_coefficients_current = 2 * np.fft.fft(current) / number_of_samples
    
    fft_coefficients_current[0] /= 2
    
    # Amplituden der DUT-Spannuns und des DUT-Stroms werden berechnet
    magnitudes_voltage_dut = np.abs(fft_coefficients_voltage_dut)
    magnitudes_current = np.abs(fft_coefficients_current)

    # Berechnet die Phasen der DUT-Spannung und dem DUT-Strom
    phases_voltage_dut = np.angle(fft_coefficients_voltage_dut)
    phases_current = np.angle(fft_coefficients_current) 
    
    # Daten der aktuellen Frequenz werden ausgegeben
    print(f"Current frequency: {current_freq} Hz")

    print(f"Magnitude of DC component of voltage: {magnitudes_voltage_dut[0]} mV")
    print(f"Magnitude of DC component of current: {magnitudes_current[0]} mA")

    # Position der Werte der aktuellen Frequenz wird berechnet
    index = int(current_freq / df)

    Rs = int(shunt_value)
    R0 = 10^12 
    C0 = 5.5e-12
    
    fft_coefficients_dut_new = (((fft_coefficients_voltage1[index]*Rs*R0)/fft_coefficients_voltage2[index]) - Rs*R0) / (Rs+R0+1j*current_freq*2*math.pi*Rs*R0*C0)
    amplitude_new = np.abs(fft_coefficients_dut_new)
    phase_new = np.angle(fft_coefficients_dut_new)

    print(amplitude_new)
    print(phase_new)
    
    mag1 = np.abs(fft_coefficients_voltage1)
    mag2 = np.abs(fft_coefficients_voltage2)
    print("last amplitude", np.abs(fft_coefficients_voltage2[-1]))
    spannungsverhältnis.append(mag2[index] / mag1[index])
    

    # Phasen werden in Grad umgerechnet
    phase_voltage_dut = np.rad2deg(phases_voltage_dut[index])
    phase_current = np.rad2deg(phases_current[index])

    print(f"Magnitude of voltage: {magnitudes_voltage_dut[index]} mV")
    print(f"Magnitude of current: {magnitudes_current[index]} mA")
    print(f"Phase of voltage: {phase_voltage_dut} degrees")
    print(f"Phase of current: {phase_current} degrees")

    # Berechnet die Amplitude und die Phase der Impedanz bei der aktuellen Frequenz
    magnitude_impedance_dut = magnitudes_voltage_dut[index] / magnitudes_current[index]
    phase_impedance_dut = phase_voltage_dut - phase_current
    if abs(phase_impedance_dut -last_phase) > 300:
        if last_phase > 0:
            phase_impedance_dut += 360
        else:
            phase_impedance_dut -= 360
        
    last_phase = phase_impedance_dut    

    # if phase_voltage_dut < 0 and phase_current > 0:
    #     phase_voltage_dut += 360

    # elif phase_voltage_dut > 0 and phase_current < 0:
    #     phase_current += 360

         
    
    # Phase der Impedanz wird zurückgerechnet auf radian
    phase_in_rad = np.deg2rad(phase_impedance_dut)
    
    # Real- und Imaginärteil derImpedanz werden für das Nyquist Diagramm berechnet
    real = magnitude_impedance_dut * np.cos(phase_in_rad)
    imag = magnitude_impedance_dut * np.sin(phase_in_rad)

    print(f"Magnitude of Impedance: {magnitude_impedance_dut} Ohm")
    print(f"Phase of Impedance: {phase_impedance_dut} degrees")

    # Werte der aktuellen Frequenz werden zur Gesamtmessung hinzugefügt
    frequencies.append(current_freq)
    magnitudes.append(magnitude_impedance_dut)
    phases.append(phase_impedance_dut)
    real_parts.append(real)
    imag_parts.append(imag)
        
# Visualisiert den Amplituden und Phasengang der Messung
fig, ax = plt.subplots(2, 2, figsize=(12, 7))
plt.subplots_adjust(hspace=0.5, wspace=0.5)

ax[0][0].scatter(real_parts, imag_parts)
ax[0][0].set_title("Nyquist-Diagramm")
ax[0][0].set_xlabel("Realteil")
ax[0][0].set_ylabel("Imaginärteil")
# ax[0][0].set_xlim(100, 700)
# ax[0][0].set_ylim(-120, 0)

# ax[1][0].scatter(real_parts, imag_parts)
# ax[1][0].set_title("Nyquist-Diagramm")
# ax[1][0].set_xlabel("Realteil")
# ax[1][0].set_ylabel("Imaginärteil")

ax[1][0].semilogx(frequencies, spannungsverhältnis)
ax[1][0].set_title("U2 / U0")
ax[1][0].set_xlabel("Frequenz (Hz)")
ax[1][0].set_ylabel("Verhältnis von U2 / U0")
ax[1][0].set_ylim(0, 0.6)
ax[1][0].set_xscale("log")


ax[0][1].scatter(frequencies, magnitudes)
ax[0][1].set_title("Amplitudengang")
ax[0][1].set_xlabel('Frequenz (Hz)')
ax[0][1].set_ylabel("Amplitude (Ohm)")
ax[0][1].set_xscale("log")
# ax[0][1].set_ylim(100, 700)

ax[1][1].scatter(frequencies, phases)
ax[1][1].set_title("Phasengang")
ax[1][1].set_xlabel('Frequenz (Hz)')
ax[1][1].set_ylabel("Phase (°)")
ax[1][1].set_xscale("log")
# ax[1][1].set_ylim(-12, 0)

plt.show()

# indices = [0, 9, 49, 99]

# for index in indices:
#     print(spannungsverhältnis[index]

# for i in range(len(spannungsverhältnis)):
#     print(frequencies[i], spannungsverhältnis[i])

border = 0.99 * spannungsverhältnis[0]
for i in range(len(spannungsverhältnis)):
    if spannungsverhältnis[i] < border:
        print("Under border at:", frequencies[i], "Hz")
        print(100 - (magnitudes[0] / magnitudes[i] * 100), "Prozent") 
        break


# for i in range(len(magnitudes)):
#     print(magnitudes[i] / magnitudes[0] * 100) 