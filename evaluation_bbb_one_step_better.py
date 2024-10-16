import numpy as np
import matplotlib.pyplot as plt
import math
import os
import re
from scipy import signal, stats
from scipy.stats import trim_mean


file_path = r"C:\Users\jonas\Desktop\Teamprojektarbeit\Aktuell\Messungen BBB\geht\1kOhm\step94.txt"

last_phase = 0

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

# Anzahl der Dateipunkte wird über Periodenanzahl bestimmt
periods_wanted = 10
number_of_samples = periods_wanted * (sample_freq // current_freq)

# Datenwerte werden in Gesamtspannung (voltage1) und Shuntspannung (voltage2) geteilt
voltage1 = []
voltage2 = []

number_of_samples = len(data)

for i in range(number_of_samples):
        first, second = data[i].split()
        voltage1.append(int(first))
        voltage2.append(int(second))

# proportiontocut = 0.1  # Proportion of values to cut
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
current = list(map(lambda x: x / 100, voltage2))

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
if abs(phase_impedance_dut - last_phase) > 100:
    phase_impedance_dut -= 360
    
last_phase = phase_impedance_dut    

# Phase der Impedanz wird zurückgerechnet auf radian
phase_in_rad = np.deg2rad(phase_impedance_dut)

# Real- und Imaginärteil derImpedanz werden für das Nyquist Diagramm berechnet
real = magnitude_impedance_dut * np.cos(phase_in_rad)
imag = magnitude_impedance_dut * np.sin(phase_in_rad)

print(f"Magnitude of Impedance: {magnitude_impedance_dut} Ohm")
print(f"Phase of Impedance: {phase_impedance_dut} degrees")


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

# magnitudes_impedance = magnitudes_voltage_dut / magnitudes_current



print(f"Magnitude of Impedance: {magnitude_impedance_dut} Ohm")
print(f"Phase of Impedance: {phase_impedance_dut} degrees")

# plt.plot(frequency_vector, magnitudes_voltage_dut)
# plt.plot(frequency_vector, magnitudes_current)
# plt.xlim(0,current_freq*2)
# plt.show()

fig, ax = plt.subplots(2,2, figsize=(8,6))
ax[0][0].plot(time_vector, voltage1)
ax[0][0].plot(time_vector, current)

ax[0][1].semilogx(frequency_vector, magnitudes_voltage_dut)
ax[0][1].semilogx(frequency_vector, magnitudes_current)

ax[1][0].plot(magnitudes_voltage_dut)
ax[1][0].plot(magnitudes_current)
# ax[1][0].semilogx(frequency_vector, magnitudes_impedance)
# ax[1][0].semilogx(frequency_vector, magnitudes_current)

    
plt.show()


