import math
import matplotlib.pyplot as plt
import numpy as np


# from tqdm import tqdm

def main():
    # Define frequency boundaries
    min_frequency = 1
    max_frequency = 1000000

    freq = 1e2

    freq_array = []
    for i in range(7):
        freq_array.append(10 ** i)

    Rdut = 1e6
    Rs = 1e6

    R_array = []
    Rs_array = []

    for i in range(12):
        R_array.append((10 ** i, 10 ** i))
        Rs_array.append(10 ** i)

    Ro = 1e12
    Ro = 83000

    Co = 4e-9

    # Define arrays for the resulting impedance values and frequencies
    results = []
    frequencies = []

    # or freq in tqdm(range(min_frequency, max_frequency)):
    # print(freq)
    result = (Rs * Ro) / math.sqrt(
        ((Rs * Ro) + Rdut * (Rs + Ro)) ** 2 + (2 * math.pi * freq * Rs * Ro * Rdut * Co) ** 2)
    # results.append(result)
    # frequencies.append(freq)

    for freq in freq_array:
        results = []
        for Rdut, Rs in R_array:
            results.append((Rs * Ro) / math.sqrt(
                ((Rs * Ro) + Rdut * (Rs + Ro)) ** 2 + (2 * math.pi * freq * Rs * Ro * Rdut * Co) ** 2))
            # results.append((Rs) / math.sqrt((Rs + Rdut)**2 + (2 * math.pi * freq * Rs * Rdut * Co)**2))

        # plt.plot(Rs_array, results)
        print(results)
        plt.semilogx(Rs_array, results, label=f"freq = {freq} Hz")
        plt.xlabel("Resistance in Ohm")
        plt.ylabel("Voltage drop")
        plt.legend()

    plt.show()

    # # Create a figure with 3 subplots
    # fig, ax = plt.subplots(3, 1, figsize=(10, 7))
    # plt.subplots_adjust(hspace=0.5)

    # # Plot the real and imaginary parts of the complex values
    # ax[0].plot(real, imag, 'b')
    # ax[0].set_xlabel('Real')
    # ax[0].set_ylabel('Imaginary')
    # ax[0].grid(True)

    # # Plot the magnitude response on a logarithmic scale
    # ax[1].semilogx(frequencies, 20*np.log10(mag), 'b')
    # # ax[1].plot(frequencies, mag, 'b')
    # ax[1].set_xlabel('Frequency (Hz)')
    # ax[1].set_ylabel('Magnitude (dB)')
    # ax[1].grid(True)

    # # Plot the phase response on a logarithmic scale
    # ax[2].semilogx(frequencies, phase, 'r')
    # ax[2].set_xlabel('Frequency (Hz)')
    # ax[2].set_ylabel('Phase (rad)')
    # ax[2].grid(True)

    # plt.show()


if __name__ == '__main__':
    main()