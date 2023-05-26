import numpy as np
import matplotlib.pyplot as plt

duration = 3  # duration of the signal in seconds
sampling_rate = 1001  # number of samples per second
num_samples = duration * sampling_rate
t = np.linspace(0, duration, num_samples, endpoint=False)

signal1 = 10 * np.sin(2 * np.pi * 1000 * t + 0)
signal2 = 3 * np.sin(2 * np.pi * 1000 * t + np.pi)
difference = signal1 - signal2

plt.plot(signal1)
plt.plot(signal2)
plt.plot(difference)

plt.show()