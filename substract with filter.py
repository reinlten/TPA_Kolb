import time
import matplotlib.pyplot as plt

start = time.time()

file = open("1_Messung 10-90Hz/step1.txt", "r")
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

# x axis values
for i in range(0,len(signal1)):
    t.append(i)


# filtering: if the derivative deviates to strong from values from before, the values will be adjusted.
dsig1 = signal1[0]-signal1[1]
i = 0
#while i < len(signal1)-10:
#    i = i + 1
#    if dsig1+20 > abs(signal1[i]-signal1[i+1]) > dsig1-20:
#        dsig1 = abs(signal1[i]-signal1[i+1])
#    else:
#        #print(f"values around i: {signal1[i-1]},{signal1[i]},{signal1[i+1]}")
#        signal1[i+1] = 2*signal1[i]-signal1[i-1]
#        dsig1 = abs(signal1[i] - signal1[i + 1])
#        #print(f"index: {i}")
#        #print(f"values around i: {signal1[i-1]},{signal1[i]},{signal1[i+1]}")
#        #print()
#        i = i+1
signal11 = []

for s in signal1:
    signal11.append(s)

if len(signal1) == len(signal11):
    print("same dim!")
else:
    print(f"not same dim! dim1 = {len(signal1)}, dim11 = {len(signal11)}")

for j in range(0,10):
    for i in range(1000,len(signal11)-1000):
        signal11[i] = sum(signal11[i-1000:i+1000])/2000


#dsig1 = signal1[0]-signal1[1]

#for i in range(1, len(signal1)-1):
#    if dsig1+10 > abs(signal1[i]-signal1[i+1]) > dsig1-10:
#        dsig1 = abs(signal1[i]-signal1[i+1])
#    else:
#        #signal1[i+1] = 2*signal1[i]-signal1[i-1]
#        print(f"index: {i}")
#        #print(f"values around i: {signal1[i-1]},{signal1[i]},{signal1[i+1]}")

# plotting the points
plt.plot(t, signal1)
plt.plot(t, signal11)

# naming the x axis
plt.xlabel('x - axis')
# naming the y axis
plt.ylabel('y - axis')

# giving a title to my graph
plt.title('cleaned')

# function to show the plot
plt.show()



end = time.time()

print("calc time: " + '{:5.3f}s'.format(end - start))
