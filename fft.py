import time
import numpy as np
from numpy.fft import fft, ifft
import matplotlib.pyplot as plt
import time
import matplotlib.pyplot as plt
import scipy.signal as signal

start = time.time()

file = open("Messungen (neu)/14.12.2022_AP_1/10k - 100k/step4.txt", "r")
data = file.readlines()

messdaten_14122022_10k_100k = [-2.64, -5.47, -7.97, -11.25, -14.4, -17.3,-20.62]


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

t = []

# get values for sampling rate and frequency
freq = int(data[0].split(" ")[0])
sampling = int(data[0].split(" ")[1])

# get number of samples in one period
period = int(sampling / freq)
print("period: " + str(period))


# fill in arrays
for d in data[1:]:
    signal1.append(int(d.split(" ")[0]))
    signal2.append(int(d.split(" ")[1]))

#TODO cutoff autom. bestimmen je nach abtastfrequenz und tatsächlicher frequenz
kern = signal.firwin(2047, cutoff = 0.01, window = "hamming")
signal11 = signal.lfilter(kern, 1, signal1)[10000:]
signal21 = signal.lfilter(kern, 1, signal2)[10000:]

# amplitude via max/min
for i in range(0, int(len(signal11) / period) + 1):
    max1.append(max(signal11[i * period:(i + 1) * period]))
    min1.append(min(signal11[i * period:(i + 1) * period]))
    max2.append(max(signal21[i * period:(i + 1) * period]))
    min2.append(min(signal21[i * period:(i + 1) * period]))

# average maximum
am1 = sum(max1) / len(max1)
am2 = sum(max2) / len(max2)

y_shift_1 = (sum(max1) / len(max1) + sum(min1) / len(min1)) / 2
y_shift_2 = (sum(max2) / len(max2) + sum(min2) / len(min2)) / 2

amplitude1 = (am1 - (sum(min1) / len(min1))) / 2
amplitude2 = (am2 - (sum(min2) / len(min2))) / 2

print("amp sig1: " + str(amplitude1))
print("amp sig2: " + str(amplitude2))


scale = amplitude2/amplitude1


signal1_shifted = [] #and scaled
signal2_shifted = []

# set up signals on same y-level and same scale.
for i in range(0, len(signal11)):
    signal1_shifted.append(scale*(signal11[i]-y_shift_1))
    signal2_shifted.append(signal21[i]-y_shift_2)

#TODO: Zeit ordentlich anpassen

# x axis values
for i in range(0,len(signal1_shifted)):
    t.append(i)

#Differenz der beiden signale bilden
subst = []

for i in range(0, len(signal1_shifted)):
    subst.append(signal2_shifted[i]-signal1_shifted[i]) #bin ich ned so davon begeistert

plt.plot(t[10000:200000], signal1_shifted[10000:200000])
plt.plot(t[10000:200000], signal2_shifted[10000:200000])
plt.plot(t[10000:200000], subst[10000:200000])
# naming the x axis
plt.xlabel('x - axis')
# naming the y axis
plt.ylabel('y - axis')
# giving a title to my graph
plt.title('cleaned')
# function to show the plot
plt.show()


#print(subst[10000:20000])
# TODO: funktioniert überhaupt nicht!!!!! Bei Messung/step1 kommt eine
#  Amplitude von 1.000.000 raus, des kann niemals passen
#  (in Octave warens um die 1000).

X = fft(subst)
N = len(X)
n = np.arange(N)
T = N/sampling
freq = n/T

plt.figure(figsize = (12, 6))
plt.subplot(121)

c1 = 2*np.abs(X)/len(subst)
c1[0] = X[0]/len(subst)

plt.stem(freq, c1, 'b',
         markerfmt=" ", basefmt="-b")
plt.xlabel('Freq (Hz)')
plt.ylabel('FFT Amplitude |X(freq)|')
#plt.xlim(0, 1100)

end = time.time()
print("calc time: " + '{:5.3f}s'.format(end - start))

plt.show()


