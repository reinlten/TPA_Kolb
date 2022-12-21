import math
import matplotlib.pyplot as plt
import numpy as np
# from tqdm import tqdm

# Defines the electrical components by returning each impedance at a given frequency
def resistor(value):
    return value

def capacitor(value, frequency):
    return 1 / (1j * (2 * math.pi * frequency) * value)

def inductor(value, frequency):
    return 1j * (2 * math.pi * frequency) * value

def series(impedance_1, impedance_2):
    return impedance_1 + impedance_2
    
def parallel(impedance_1, impedance_2):
    return (impedance_1 * impedance_2) / (impedance_1 + impedance_2)

def circuit_1(frequency, r1, r2, r3, c1):
    return series(parallel(resistor(r2), series(resistor(r1), capacitor(c1, frequency))), resistor(r3))
    
def circuit_test(frequency, r1, c1):
    return series(resistor(r1), capacitor(c1, frequency))
    
    
def main():
    # Define frequency boundaries
    min_frequency = 1
    max_frequency = 1000000
    
    # Define values of components that are being used in the circuit
    r1 = 1000
    r2 = 560
    r3 = 100
    c1 = 180 * 10**-12
    
    # Define arrays for the resulting impedance values and frequencies
    results = []
    frequencies = []
    
    # Calculates the resulting impedance in the given frequency interval
    for freq in range(min_frequency, max_frequency):
        result = circuit_1(freq, r1, r2, r3, c1)
        results.append(result)
        frequencies.append(freq)
    
    # Same function but with progress bar
    # for freq in tqdm(range(min_frequency, max_frequency)):
    #     result = circuit_1(freq, r1, r2, r3, c1)
    #     results.append(result)
    #     frequencies.append(freq)
    

    # Calculate the real and imaginary parts of the result
    real = [x.real for x in results]
    imag = [x.imag for x in results]
    
    # Calculate the magnitude and phase of the results
    mag = [abs(x) for x in results]
    phase = [np.angle(x) for x in results]
    

    # Create a figure with 3 subplots
    fig, ax = plt.subplots(3, 1, figsize=(10, 7))
    plt.subplots_adjust(hspace=0.5)
    
    # Plot the real and imaginary parts of the complex values
    ax[0].plot(real, imag, 'b')
    ax[0].set_xlabel('Real')
    ax[0].set_ylabel('Imaginary')
    ax[0].grid(True)
    
    # Plot the magnitude response on a logarithmic scale
    ax[1].semilogx(frequencies, 20*np.log10(mag), 'b')
    ax[1].set_xlabel('Frequency (Hz)')
    ax[1].set_ylabel('Magnitude (dB)')
    ax[1].grid(True)
    
    # Plot the phase response on a logarithmic scale
    ax[2].semilogx(frequencies, phase, 'r')
    ax[2].set_xlabel('Frequency (Hz)')
    ax[2].set_ylabel('Phase (rad)')
    ax[2].grid(True)
    
    plt.show()
    
 
    
if __name__ == '__main__':
    main()