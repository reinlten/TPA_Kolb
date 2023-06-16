import math
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

def main():

    
    # Define frequency boundaries
    min_frequency = 1
    max_frequency = 1000000

    input_voltage = 550

    Rdut = 120
    Rs = 120

    Ro = 1000
    Co = 4*10**-12

    # Define arrays for the resulting impedance values and frequencies
    results = []
    frequencies = []
    voltages = []

    for freq in tqdm(range(min_frequency, max_frequency)):
        # print(freq)
        result = (Rs * Ro) / math.sqrt(((Rs * Ro) + Rdut * (Rs + Ro))**2 + (2 * math.pi * freq * Rs * Ro * Rdut * Co)**2)
        results.append(result)
        voltages.append(input_voltage * result)
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
    ax[0].semilogx(frequencies, voltages)
    # ax[0].set_xlabel('Real')
    # ax[0].set_ylabel('Imaginary')
    # ax[0].grid(True)

    # Plot the magnitude response on a logarithmic scale
    ax[1].semilogx(frequencies, 20*np.log10(voltages))
    # ax[1].plot(frequencies, mag, 'b')
    # ax[1].set_xlabel('Frequency (Hz)')
    # ax[1].set_ylabel('Magnitude (dB)')
    # ax[1].grid(True)

    # Plot the phase response on a logarithmic scale
    ax[2].semilogx(frequencies, results)
    # ax[2].set_xlabel('Frequency (Hz)')
    # ax[2].set_ylabel('Phase (rad)')
    # ax[2].grid(True)

    plt.show()

 
    
if __name__ == '__main__':
    main()