import csv
import matplotlib.pyplot as plt
import numpy as np

# Path of the file that is being analized
filepath = r"C:\Users\jonas\Desktop\TPA_Kolb\Oszilloskop Messungen 19.4.23\WA000001.CSV"

number_of_samples = 9000

# Reads in the file
with open(filepath, 'r') as file:
    reader = csv.reader(file)
    
    lines = []
    
    for row in reader:
        lines.append(row)     

file.close()

# Splits the lines in Header and Data
header = lines[:10]
data = lines[10:number_of_samples + 10]


# Splits the data in seperate arrays
time = []
voltage_total = []
voltage_shunt = []
for line in data:
    time.append(float(line[3]))
    voltage_total.append(float(line[4]))
    voltage_shunt.append(float(line[5]))

# Calculates the fft coefficients of each voltage signal    
fft_coeff_voltage_total = 2 * np.fft.fft(voltage_total) / len(data)
fft_coeff_voltage_shunt = 2 * np.fft.fft(voltage_shunt) / len(data)

fft_coeff_voltage_total[0] /= 2
fft_coeff_voltage_shunt[0] /= 2

fft_coeff_voltage_dut = []
for i in range(len(fft_coeff_voltage_total)):
    fft_coeff_voltage_dut.append(fft_coeff_voltage_total[i] - fft_coeff_voltage_shunt[i])

# Calculates the current and its fft coefficients from the shunt voltage signal
current = list(map(lambda x: x / 100, voltage_shunt))

fft_coeff_current = 2 * np.fft.fft(current) / len(data)

fft_coeff_current[0] /= 2

# Calculates the magnitudes and phases of the voltage and current of the DUT
magnitudes_voltage_dut = np.abs(fft_coeff_voltage_dut)
magnitudes_current = np.abs(fft_coeff_current)

phases_voltage_dut = np.angle(fft_coeff_voltage_dut)
phases_current = np.angle(fft_coeff_current) 

sample_frequency = 1000000000
df = sample_frequency / number_of_samples
frequency_vector = np.arange(0, number_of_samples * df, df)

# Creates the plots
fig, ax = plt.subplots(2, 2, figsize=(12, 7))
ax[0][0].plot(time, voltage_total, label='Total Voltage')
ax[0][0].plot(time, voltage_shunt, label='Shunt Voltage')
ax[0][0].legend()

ax[0][1].semilogx(frequency_vector, magnitudes_voltage_dut, label="Magnitudes DUT")
ax[0][1].semilogx(frequency_vector, magnitudes_current, label="Magnitudes Current")
ax[0][1].legend()


magnitude_impedance = max(magnitudes_voltage_dut) / max(magnitudes_current)
print(magnitude_impedance)

plt.show()

