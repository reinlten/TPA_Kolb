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

print("amp sig1: " + str(amplitude1))
print("amp sig2: " + str(amplitude2))

# test to get phase shift with maximums, not zeros.
for i in range(0, len(signal1)):
    if signal1[i] == max1[int(i / period)]:
        index_max1.append(i)
    if signal2[i] == max2[int(i / period)]:
        index_max2.append(i)

# print(index_max1)

# zero line of both signals are evaluated below
zero1 = []
zero2 = []

for i in range(0, int(len(signal1) / period) + 1):
    zero1.append((max(signal1[i * period:(i + 1) * period]) + min(signal1[i * period:(i + 1) * period])) / 2)
    zero2.append((max(signal2[i * period:(i + 1) * period]) + min(signal2[i * period:(i + 1) * period])) / 2)

z1 = sum(zero1) / len(zero1)
z2 = sum(zero2) / len(zero2)

temp1 = []
temp2 = []
c1 = 0
c2 = 0
for i in range(0, len(signal1)):
    # allow a 0.5% tolerance around zero
    if z1 - amplitude1 * amp_tolerance <= signal1[i] <= z1 + amplitude1 * amp_tolerance:
        if c1 != 0:
            # check the range for the next value (if too far, it must be the next zero)
            if int(i - temp1[c1 - 1] > 0.3 * period):
                signal_zero1.append(int(sum(temp1) / len(temp1)))
                temp1 = []
                c1 = 0
            else:
                temp1.append(i)
                c1 += 1
        else:
            temp1.append(i)
            c1 += 1

    # allow a 0.5% tolerance around zero
    if z2 - amplitude2 * amp_tolerance <= signal2[i] <= z2 + amplitude2 * amp_tolerance:
        if c2 != 0:
            # check the range for the next value (if too far, it must be the next zero.
            # the next zero must be around 0.5*period, we give a 0.2 tolerance.
            if int(i - temp2[c2 - 1] > 0.3 * period):
                signal_zero2.append(int(sum(temp2) / len(temp2)))
                temp2 = []
                c2 = 0
            else:
                temp2.append(i)
                c2 += 1
        else:
            temp2.append(i)
            c2 += 1

phase_array = []
# print(signal_zero1)
# print(signal_zero2)
# print(len(signal_zero1))
# print(len(signal_zero2))

# evaluate phase shift
# check sum
if len(signal_zero1) == len(signal_zero2):
    for i in range(0, len(signal_zero2)):
        phase_array.append(abs(signal_zero2[i] - signal_zero1[i]))

    print("phase shift: " + str(sum(phase_array) / len(phase_array)) + " (" +
          str(360 * (sum(phase_array) / len(phase_array)) / period) + "°)" +
          " (tol%: " + str(amp_tolerance) + ")")

else:
    print("wrong checksum")
    # TODO: averaging function if sth goes wrong
    print(len(signal_zero1))
    print(len(signal_zero2))
    print(signal_zero1)
    print(signal_zero2)

end = time.time()
print("calc time: " + '{:5.3f}s'.format(end - start))
