import time




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

# set up signals on same y-level and same scale.
for i in range(0, len(signal1)):
    signal1_shifted.append(int(signal1[i]-y_shift_1))
    signal2_scaled_shifted.append(int(scale*(signal2[i]-y_shift_2)))


max1 = []
max2 = []
min1 = []
min2 = []

for i in range(0, int(len(signal1) / period) + 1):
    max1.append(max(signal1_shifted[i * period:(i + 1) * period]))
    min1.append(min(signal1_shifted[i * period:(i + 1) * period]))
    max2.append(max(signal2_scaled_shifted[i * period:(i + 1) * period]))
    min2.append(min(signal2_scaled_shifted[i * period:(i + 1) * period]))

print(min1)
print(min2)

korr = []
temp_sum = []

# shift signal2 k steps and subtract signal1. Smallest sum wins
# this is probably slow. Gradient decent advisable (2 fors -> not good.
# runtime with k = -50..50: 48,744s).
for k in range(1895,1905,1):
    for i in range(0,len(signal1)-abs(k)):
        if k < 0:
            temp_sum.append(signal1_shifted[i-k] - signal2_scaled_shifted[i])
        else:
            temp_sum.append(signal1_shifted[i] - signal2_scaled_shifted[i+k])

    korr.append(sum(temp_sum))
    temp_sum = []

end = time.time()

print(korr)
print(min(korr))
for i in range(len(korr)):
    if korr[i] == min(korr):
        print(i+1895)

print("calc time: " + '{:5.3f}s'.format(end - start))
