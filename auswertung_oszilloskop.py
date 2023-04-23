import csv
import matplotlib.pyplot as plt
import numpy as np

filepath = r"C:\Users\jonas\Desktop\TPA_Kolb\Oszilloskop Messungen 19.4.23\WA000001.CSV"

with open(filepath, 'r') as file:
    reader = csv.reader(file)
    
    lines = []
    
    for row in reader:
        lines.append(row)     

file.close()

header = lines[:10]
data = lines[10:]

# print(header)
# print(data[0])
time = []
voltage_total = []
voltage_shunt = []
for line in data:
    time.append(float(line[3]))
    voltage_total.append(float(line[4]))
    voltage_shunt.append(float(line[5]))
    
# voltage_dut = []
# for i in range(len(voltage_total)):
#     voltage_dut.append(voltage_total[i] - voltage_shunt[i])  

    
fft_coeff_voltage_total = 2 * np.fft.fft(voltage_total) / len(data)
fft_coeff_voltage_shunt = 2 * np.fft.fft(voltage_shunt) / len(data)

fft_coeff_voltage_total[0] / 2
fft_coeff_voltage_shunt[0] / 2

fft_coeff_voltage_dut = []
for i in range(len(fft_coeff_voltage_total)):
    fft_coeff_voltage_dut.append(fft_coeff_voltage_total[i] - fft_coeff_voltage_shunt[i])

current = list(map(lambda x: x / 100, voltage_shunt))

fft_coeff_current = 2 * np.fft.fft(current) / len(data)

magnitudes_voltage_dut = np.abs(fft_coeff_voltage_dut)
magnitudes_current = np.abs(fft_coeff_current)

phases_voltage_dut = np.angle(fft_coeff_voltage_dut)
phases_current = np.angle(fft_coeff_current) 


fig, ax = plt.subplots(2, 2, figsize=(12, 7))
ax[0][0].plot(time, voltage_total, label='Total Voltage')
ax[0][0].plot(time, voltage_shunt, label='Shunt Voltage')
ax[0][0].legend()

ax[0][1].semilogx(time, magnitudes_voltage_dut, label="Magnitudes DUT")
ax[0][1].semilogx(time, magnitudes_current, label="Magnitudes Current")
ax[0][1].legend()

magnitude_impedance = max(magnitudes_voltage_dut) / max(magnitudes_current)
print(magnitude_impedance)
# ax[1][0].semilogx(frequency_vector, magnitudes_impedance)
# ax[1][0].semilogx(frequency_vector, magnitudes_current)

# plt.show()

