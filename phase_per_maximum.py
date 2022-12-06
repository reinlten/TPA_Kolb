import time

start = time.time()

file = open("Messdaten/step1.txt", "r")
data = file.readlines()

# init arrays
signal1 = []
signal2 = []

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

amp_tolerance = 0.005

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

# average maximum
am1 = sum(max1) / len(max1)
am2 = sum(max2) / len(max2)

amplitude1 = (am1 - (sum(min1) / len(min1))) / 2
amplitude2 = (am2 - (sum(min2) / len(min2))) / 2

print("amp sig1: " + str(amplitude1))
print("amp sig2: " + str(amplitude2))

# test to get phase shift with maximums, not zeros.
temp1 = []
temp2 = []
c1 = 0
c2 = 0

for i in range(0, len(signal1)):
    if signal1[i] >= (1-amp_tolerance)*am1:
        if c1 != 0:
            if i - temp1[c1-1] > 0.3 * period:
                index_max1.append(int(sum(temp1) / len(temp1)))
                temp1 = []
                c1 = 0
            else:
                temp1.append(i)
                c1 += 1
        else:
            temp1.append(i)
            c1 += 1

    if signal2[i] >= (1 - amp_tolerance) * am2:
        if c2 != 0:
            if i - temp2[c2 - 1] > 0.3 * period:
                index_max2.append(int(sum(temp2) / len(temp2)))
                temp2 = []
                c2 = 0
            else:
                temp2.append(i)
                c2 += 1
        else:
            temp2.append(i)
            c2 += 1

phase_array = []

if len(index_max1) == len(index_max2):
    for i in range(0, len(index_max2)):
        phase_array.append(abs(index_max1[i] - index_max2[i]))

    print("phase shift: " + str(sum(phase_array) / len(phase_array)) + " (" +
          str(360 * (sum(phase_array) / len(phase_array)) / period) + "°)" +
          " (tol%: " + str(amp_tolerance) + ")")

else:
    print("wrong checksum")
    # TODO: averaging function if sth goes wrong
    print(index_max1)
    print(index_max2)
    print(len(index_max1))
    print(len(index_max2))


end = time.time()
print("calc time: " + '{:5.3f}s'.format(end - start))
