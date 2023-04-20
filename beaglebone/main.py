import measurement
import numpy as np
import matplotlib.pyplot as plt
import math

def main():
    print("Test")
    
    # Sets the path of the textfile of the measurement
    file_path = r"C:\Users\jonas\Desktop\Teamprojektarbeit\Aktuell\Messungen BBB\07.02.2023_1\100kHz - 1MHz\step1.txt"
    
    # Sets the number of samples that are used
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
   
    dt = 1 / sample_freq
    df = sample_freq / number_of_samples
    time_vector = np.arange(0, number_of_samples * dt, dt)
    frequency_vector = np.arange(0, number_of_samples * df, df)
    
    fft_coefficients_voltage1 = 2 * np.fft.fft(voltage1) / number_of_samples
    fft_coefficients_voltage2 = 2 * np.fft.fft(voltage2) / number_of_samples

    fft_coefficients_voltage1[0] /= 2
    fft_coefficients_voltage2[0] /= 2
    
    # Berechnet die Amplitude der FFt Koeffizienten
    # mag1 = np.abs(fft_coefficients_voltage1)
    # mag2 = np.abs(fft_coefficients_voltage2)

    # Berechnet die Phase der FFT Koeffizienten
    # phase1 = np.angle(fft_coefficients_voltage1)
    # phase2 = np.angle(fft_coefficients_voltage2)

    # plt.plot(frequency_vector, mag1)
    # plt.plot(frequency_vector, mag2)
    # plt.show()

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

    fig, ax = plt.subplots(2,2, figsize=(8,6))
    ax[0][0].plot(time_vector, voltage1)
    ax[0][0].plot(time_vector, current)

    ax[0][1].semilogx(frequency_vector, magnitudes_voltage_dut)
    ax[0][1].semilogx(frequency_vector, magnitudes_current)

    # ax[1][0].semilogx(frequency_vector, magnitudes_impedance)
    # ax[1][0].semilogx(frequency_vector, magnitudes_current)

    plt.show()

if __name__ == "__main__":
    main()