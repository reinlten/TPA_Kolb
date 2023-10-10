import numpy as np
import matplotlib.pyplot as plt
import os
import re



# Pfad in dem die Ordner mit den Messungen liegen
measurement_path = r"C:\Users\jonas\Desktop\Teamprojektarbeit\Aktuell\Messungen BBB\08.08.2023\1"
shunt_value = 100

# Arrays für die Speicherung wichtiger Werte
magnitudes = []
phases = []
frequencies = []
real_parts = []
imag_parts = []
last_phase = 0
amplitudenverhältnis = []
phasenverhältnis = []
# c1 = []
# c2 = []


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
    print(f"\nAktuelle Frequenz: {current_freq} Hz")

    # Gleichanteile werden ausgegeben
    print(f"Gleichanteil der Spannung: {magnitudes_voltage_dut[0]} mV")
    print(f"Gleichanteil des Stroms: {magnitudes_current[0]} mA")

    # Position der Werte der aktuellen Frequenz wird berechnet
    index = int(current_freq / df)

    # Amplituden der aktuellen Frequenz werden berechnet
    mag1 = np.abs(fft_coefficients_voltage1)
    mag2 = np.abs(fft_coefficients_voltage2)
    amplitudenverhältnis.append(mag2[index] / mag1[index])

    # Phasen der aktuellen Frequenz werden berechnet
    phase1 = np.angle(fft_coefficients_voltage1)
    phase2 = np.angle(fft_coefficients_voltage2)
    phasenverhältnis.append(phase1[index] / phase2[index])

    # Phasen werden in Grad umgerechnet
    phase_voltage_dut = np.rad2deg(phases_voltage_dut[index])
    phase_current = np.rad2deg(phases_current[index])

    # Betraf und Phase der Shuntspannung und des Shuntstroms werden ausgegeben
    print(f"Betrag der Shuntspannung: {magnitudes_voltage_dut[index]} mV")
    print(f"Betrag des Shuntstroms: {magnitudes_current[index]} mA")
    print(f"Phase der Shuntspannung: {phase_voltage_dut} °")
    print(f"Phase des Shuntstroms: {phase_current} °")

    # Berechnet die Amplitude und die Phase der Impedanz bei der aktuellen Frequenz
    magnitude_impedance_dut = magnitudes_voltage_dut[index] / magnitudes_current[index]
    phase_impedance_dut = phase_voltage_dut - phase_current
    if abs(phase_impedance_dut -last_phase) > 300:
        if last_phase > 0:
            phase_impedance_dut += 360
        else:
            phase_impedance_dut -= 360
        
    last_phase = phase_impedance_dut    

    # Phase der Impedanz wird zurückgerechnet auf radian
    phase_in_rad = np.deg2rad(phase_impedance_dut)
    
    # Real- und Imaginärteil derImpedanz werden für das Nyquist Diagramm berechnet
    real = magnitude_impedance_dut * np.cos(phase_in_rad)
    imag = magnitude_impedance_dut * np.sin(phase_in_rad)

    print(f"Betrag der Impedanz: {magnitude_impedance_dut:} \u03A9")
    print(f"Phase der Impedanz: {phase_impedance_dut} °")

    # Werte der aktuellen Frequenz werden zur Gesamtmessung hinzugefügt
    frequencies.append(current_freq)
    magnitudes.append(magnitude_impedance_dut)
    phases.append(phase_impedance_dut)
    real_parts.append(real)
    imag_parts.append(imag)
    
# font = {'fontname':'Arial'}
# hfont = {'fontname':'Helvetica'}

# Ab hier Erstellung der Diagramme
fig1 = plt.figure(figsize = (8,5))
plt.scatter(frequencies, amplitudenverhältnis)
plt.xscale("log")
# plt.title("[a]", size = 15, font = "Arial")
plt.xlabel("Frequenz / Hz", size = 12)
plt.ylabel("U2/U0 / - ", size = 12)
plt.xticks(fontsize=17, font ="Arial")
plt.yticks(fontsize=17, font="Arial")
plt.ylim(0,amplitudenverhältnis[-1] * 2)
plt.savefig(r"C:\Users\jonas\Desktop\diagramme_auswertung\amplitudenverhältnis.png")

fig2 = plt.figure(figsize = (8,5))
plt.scatter(frequencies, phasenverhältnis)
plt.xscale("log")
# plt.title("[b]", size = 15)
plt.xlabel("Frequenz / Hz", size = 12)
plt.ylabel("\u03C62/\u03C61 / - ", size = 12)
plt.ylim(0,phasenverhältnis[-1] * 2)
plt.savefig(r"C:\Users\jonas\Desktop\diagramme_auswertung\phasenverhältnis.png")

fig3 = plt.figure(figsize = (8,5))
plt.scatter(frequencies, magnitudes)
plt.xscale("log")
# plt.title("[c]", size = 15)
plt.xlabel("Frequenz / Hz", size = 12)
plt.ylabel("Betrag / \u03A9 ", size = 12)
plt.ylim(0,magnitudes[-1] * 2)
plt.savefig(r"C:\Users\jonas\Desktop\diagramme_auswertung\Betragsgang.png")

fig4 = plt.figure(figsize = (8,5))
plt.scatter(frequencies, phases)
plt.xscale("log")
# plt.title("[d]", size = 15)
plt.xlabel("Frequenz / Hz", size = 12)
plt.ylabel("Phase / ° ", size = 12)
plt.ylim(0,phases[-1] * 2)
plt.savefig(r"C:\Users\jonas\Desktop\diagramme_auswertung\Phasengang.png")

fig5 = plt.figure(figsize = (8,8))
plt.scatter(real_parts, imag_parts)
# plt.xscale("log")
# plt.title("[e]", size = 15)
plt.xlabel("R / \u03A9", size = 12)
plt.ylabel("X / \u03A9 ", size = 12)
# plt.ylim(0,phases[-1] * 2)
plt.savefig(r"C:\Users\jonas\Desktop\diagramme_auswertung\Nyquist.png")

plt.show()


# for i in range(len(phasenverhältnis)):
#     print(f" c1 {c1[i]:<10.5f}   c2 {c2[i]:<10.5f}   pv {phasenverhältnis[i]:.5f}")
