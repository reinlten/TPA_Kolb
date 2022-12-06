import time
import numpy as np
from numpy.fft import fft, ifft
import matplotlib.pyplot as plt



start = time.time()

file = open("Messdaten/step1.txt", "r")
data = file.readlines()

# init arrays
signal1 = []
signal2 = []
signal3 = []


max1 = []
max2 = []
min1 = []
min2 = []

index_max1 = []
index_max2 = []

signal_zero1 = []
signal_zero2 = []

amplitude1 = 0
amplitude2 = 0

amp_tolerance = 0.2

# get values for sampling rate and frequency
freq = int(data[0].split(" ")[0])
sampling = int(data[0].split(" ")[1])

# get number of samples in one period
period = int(sampling / freq)
print("period: " + str(period))

ts = 1.0/sampling
t = np.arange(0,1,ts)

# fill in arrays
for d in data[1:]:
    signal1.append(int(d.split(" ")[0]))
    signal2.append(int(d.split(" ")[1]))

# amplitude via max/min
for i in range(0, int(len(signal1) / period) + 1):
    max1.append(max(signal1[i * period:(i + 1) * period]))
    min1.append(min(signal1[i * period:(i + 1) * period]))
    max2.append(max(signal2[i * period:(i + 1) * period]))
    min2.append(min(signal2[i * period:(i + 1) * period]))

amplitude1 = (sum(max1) / len(max1) - sum(min1) / len(min1)) / 2
amplitude2 = (sum(max2) / len(max2) - sum(min2) / len(min2)) / 2

y_shift_1 = sum(min1) / len(min1) + amplitude1
y_shift_2 = sum(min2) / len(min2) + amplitude2

print("amp sig1: " + str(amplitude1))
print("amp sig2: " + str(amplitude2))

scale = amplitude1/amplitude2

signal1_shifted = []
signal2_scaled_shifted = []

for i in range(0, len(signal1)):
    signal1_shifted.append(int(signal1[i]-y_shift_1))
    signal2_scaled_shifted.append(int(scale*(signal2[i]-y_shift_2)))
    signal3.append(int(signal1[i]-y_shift_1)-int((scale*(signal2[i]-y_shift_2))))

print(signal1_shifted[:10000])
print(signal2_scaled_shifted[:10000])
print(signal3[:10000])

# TODO: funktioniert überhaupt nicht!!!!! Bei Messung/step1 kommt eine
#  Amplitude von 1.000.000 raus, des kann niemals passen
#  (in Octave warens um die 1000).
#  Richtiges drecksverfahren, scrape it

X = fft(signal3[:100000])
N = len(X)
n = np.arange(N)
T = N/sampling
freq = n/T

plt.figure(figsize = (12, 6))
plt.subplot(121)

plt.stem(freq, np.abs(X), 'b',
         markerfmt=" ", basefmt="-b")
plt.xlabel('Freq (Hz)')
plt.ylabel('FFT Amplitude |X(freq)|')
plt.xlim(0, 1100)

end = time.time()
print("calc time: " + '{:5.3f}s'.format(end - start))

plt.show()


