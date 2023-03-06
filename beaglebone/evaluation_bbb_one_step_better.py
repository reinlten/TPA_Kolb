import numpy as np
import matplotlib.pyplot as plt
import math


file_path = r"C:\Users\jonas\Desktop\Uni\Teamprojektarbeit\Aktuell\Messungen BBB\07.02.2023_1/10kHz - 90kHz/step5.txt"

# Legt die Anzahl an Datenpunkten fest
number_of_samples = 100000

# Liest die Daten ein
with open(file_path, "r") as file:
    lines = file.readlines()

file.close()

# Speichert den Header und die Datenzeilen in verschiedene Arrrays
header_lines = []
data_lines = []

# Liest die Zeilen ein
for line in range(1):
    # Stores the header in header_lines
    header_lines.append(lines[line])
    
for line in range(1,number_of_samples + 1):
    # Stores the data in data_lines
    data_lines.append(lines[line])

# Formatiert den Header und die Datenzeilen richtig
data = []
header = []

for line in data_lines:
    data.append(line.split())

header_lines = header_lines[0].strip()
values = header_lines.split(" ")

# Extrahiert die Werte aus dem Header
current_freq = int(values[0])
sample_freq = int(values[1])
number_of_periods = int(values[2])
number_of_samples_per_period = int(values[3])

# Formatiert die Daten für die Weiterverarbeitung
for i in range(len(data)):
    data[i][1] = data[i][1].rstrip()
    data[i][0] = int(data[i][0])
    data[i][1] = int(data[i][1])

# Erstellt den Zeit- und Frequenzvektor
dt = 1 / sample_freq
df = sample_freq /number_of_samples
time_vector = np.arange(0, number_of_samples * dt, dt)
frequency_vector = np.arange(0, number_of_samples * df, df)

# print(len(data))
# print(len(time_vector))
# print(time_vector[-1])
# print(len(frequency_vector))
# print(frequency_vector[0])
# print(frequency_vector[-1])
# print(df)

# Teilt die Daten in ein Spannungs- und ein Stromarray auf
voltage1 = []
voltage2 = []

for row in data:
    voltage1.append(row[0])
    voltage2.append(row[1])
    
# Führt die FFT auf beiden Spannungssignalen aus
fft_coefficients_voltage1 = 2 * np.fft.fft(voltage1) / number_of_samples
fft_coefficients_voltage2 = 2 * np.fft.fft(voltage2) / number_of_samples

# Berechnet den Gleichanteil richtig
fft_coefficients_voltage1[0] / 2
fft_coefficients_voltage2[0] / 2

# Berechnet die Amplitude der FFt Koeffizienten
mag1 = np.abs(fft_coefficients_voltage1)
mag2 = np.abs(fft_coefficients_voltage2)

# Berechnet die Phase der FFT Koeffizienten
phase1 = np.angle(fft_coefficients_voltage1)
phase2 = np.angle(fft_coefficients_voltage2)

# plt.plot(frequency_vector, phase1)
# plt.plot(frequency_vector, phase2)
# plt.show()

# Plottet das Amplitudenspektrum der beiden Spannungen
plt.plot(frequency_vector, mag1)
plt.plot(frequency_vector, mag2)
plt.show()

# print(fft_coefficients_voltage1[:5])

# Berechnet die Spannung, die über dem DUT abfällt über Gesamtspannung - Shuntspannung
fft_coefficients_voltage_dut = []
for i in range(len(fft_coefficients_voltage1)):
    fft_coefficients_voltage_dut.append(fft_coefficients_voltage1[i] - fft_coefficients_voltage2[i])
    
# Rechnet die Spannung über dem Shunt zurück in Strom
current = list(map(lambda x: x / 100, voltage2))

# Berechnet die FFT für den Strom
fft_coefficients_current = 2 * np.fft.fft(current) / number_of_samples

# real__part_of_voltage = np.real(fft_coefficients_voltage_dut)
# real__part_of_current = np.real(fft_coefficients_current)

# imag_part_of_voltage = np.imag(fft_coefficients_voltage_dut)
# imag_part_of_current = np.imag(fft_coefficients_current)

# Berechnet die Amplitude der DUT-Spannung und dem DUT-Strom
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

# ax[1][0].semilogx(frequency_vector, magnitudes_impedance)
# ax[1][0].semilogx(frequency_vector, magnitudes_current)

    
plt.show()


