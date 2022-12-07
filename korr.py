import time




start = time.time()

file = open("1_Messung 10-90Hz/step1.txt", "r")
data = file.readlines()

a="string"
b="string: #"
if a == b:
    print("a=b")
else:
    print("anichtb")
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

print(max1)
print(max2)

print(min1)
print(min2)

amplitude1 = (sum(max1) / len(max1) - sum(min1) / len(min1)) / 2
amplitude2 = (sum(max2) / len(max2) - sum(min2) / len(min2)) / 2

y_shift_1 = (sum(max1) / len(max1) + sum(min1) / len(min1)) / 2
y_shift_2 = (sum(max2) / len(max2) + sum(min2) / len(min2)) / 2

print("amp sig1: " + str(amplitude1))
print("amp sig2: " + str(amplitude2))



scale = amplitude1/amplitude2


signal1_shifted = []
signal2_scaled_shifted = []

# set up signals on same y-level and same scale.
for i in range(0, len(signal1)):
    signal1_shifted.append(int(signal1[i]))#-y_shift_1))
    signal2_scaled_shifted.append(int(scale*(signal2[i])))#-y_shift_2)))


max1 = []
max2 = []
min1 = []
min2 = []

for i in range(0, int(len(signal1) / period) + 1):
    max1.append(max(signal1_shifted[i * period:(i + 1) * period]))
    min1.append(min(signal1_shifted[i * period:(i + 1) * period]))
    max2.append(max(signal2_scaled_shifted[i * period:(i + 1) * period]))
    min2.append(min(signal2_scaled_shifted[i * period:(i + 1) * period]))

print(signal1_shifted[:10000])
print(signal2_scaled_shifted[:10000])

korr = []
korr_steps = []
temp_sum = []
neg_shift = -100
pos_shift = 100

# shift signal2 k steps and subtract signal1. Smallest sum wins
# this is probably slow. Gradient decent advisable (2 fors -> not good.
# runtime with k = -50..50: 48,744s).

# problem mit richtigem shift bei zu geringen Periodendauern.
# TODO Shift abh. machen von änderungsrate (siehe gradient decent
#  j abhängig machen von Periodendauer.
for j in range(0, int(len(signal1)/1000000)):
    for k in range(neg_shift, pos_shift):
        for i in range(1000000*j, 1000000*(j+1)-pos_shift):
            if k < 0:
                temp_sum.append(abs(signal1_shifted[i-k] - signal2_scaled_shifted[i]))
            else:
                temp_sum.append(abs(signal1_shifted[i] - signal2_scaled_shifted[i+k]))

        korr.append(sum(temp_sum))
        temp_sum = []

    for i in range(len(korr)):
        if korr[i] == min(korr):
            korr_steps.append(i+neg_shift)
            print("verschiebung: " + str(i+neg_shift))
            # TODO das hier zum laufen bringen!!!
            # pos_shift = neg_shift + i + 200
            # neg_shift = neg_shift + i - 200


    korr = []

end = time.time()

#print(korr)
#print(min(korr))
#for i in range(len(korr)):
#    if korr[i] == min(korr):
#        print("verschiebung: " + str(i))

print(f"average shift = {sum(korr_steps)/len(korr_steps)}")

print("calc time: " + '{:5.3f}s'.format(end - start))
