import math
import matplotlib.pyplot as plt

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
    min_frequency = 1
    max_frequency = 1000000
    r1 = 1000
    r2 = 560
    r3 = 100
    c1 = 180 * 10**-12
    
    results = []
    
    for freq in range(min_frequency, max_frequency):
        result = circuit_1(freq, r1, r2, r3, c1)
        results.append(result)
        
    print(results[:10])
    real = [x.real for x in results]
    imag = [x.imag for x in results]

    # Plot the real and imaginary parts of the complex values
    plt.plot(real, imag, 'bo')
    plt.xlabel('Real')
    plt.ylabel('Imaginary')
    plt.grid(True)
    plt.show()

    
if __name__ == '__main__':
    main()