import math
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

def main():
    # Define frequency boundaries
    min_frequency = 1
    max_frequency = 1000000

    input_voltage = 550

    Rdut = 1000
    Rs = 1000

    Ro = 1000000
    Co = 4*10**-12

    # Define arrays for the resulting impedance values and frequencies
    frequencies = []
    amplitudes = []
    phases = []
    voltages = []

    for freq in tqdm(range(min_frequency, max_frequency)):
        # print(freq)
        amplitude = (Rs * Ro) / math.sqrt(((Rs * Ro) + Rdut * (Rs + Ro))**2 + (2 * math.pi * freq * Rs * Ro * Rdut * Co)**2)
        amplitudes.append(amplitude)
        phase = (-1)*np.arctan(((2 * np.pi * freq) * Rs * Ro * Rdut * Co) / (Rs * Ro + Rdut * (Rs + Ro)))
        phases.append(phase)
        
        voltages.append(input_voltage * amplitude)
        frequencies.append(freq)
    

    # x_line = [0, max_frequency]
    # y_line = [threshhold, threshhold]



    # plt.semilogx(frequencies, 20*np.log10(results))
    # plt.semilogx(frequencies, results)

    # plt.plot(x_line, y_line)

    # plt.show()

    # Create a figure with 3 subplots
    fig, ax = plt.subplots(3, 1, figsize=(10, 7))
    plt.subplots_adjust(hspace=0.5)

    # Plot the real and imaginary parts of the complex values
    ax[0].semilogx(frequencies, amplitudes)
    ax[0].set_xlabel('Frequencies in Hz')
    ax[0].set_ylabel('Amplitude of U2 / U0')
    ax[0].grid(True)

    # Plot the magnitude response on a logarithmic scale
    ax[1].semilogx(frequencies, phases)
    ax[1].set_xlabel('Frequency in Hz')
    ax[1].set_ylabel('Phase of U2 / U0')
    ax[1].grid(True)

    # Plot the phase response on a logarithmic scale
    ax[2].semilogx(frequencies, voltages)
    ax[2].set_xlabel('Frequency in Hz')
    ax[2].set_ylabel('Voltage in mV')
    ax[2].grid(True)

    plt.show()

 
    
if __name__ == '__main__':
    main()