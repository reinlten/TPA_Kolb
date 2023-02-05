import time
import matplotlib.pyplot as plt
import scipy.signal as signal
import math

data = ["step1.txt", "step2.txt","step3.txt", "step4.txt","step5.txt","step6.txt","step7.txt","step8.txt","step9.txt","step10.txt"]
phases = []

for d in data:
    start = time.time()

    file = open(f"Messungen (neu)/14.12.2022_AP_1/100k - 1M/{d}", "r")
    data = file.readlines()
    file.close()

    messdaten_14122022_10k_100k = [-0.4496538461538462, -0.29423076923076924, -0.6916845530706917, -1.0163076923076924, -1.331826923076923, -1.610259488410749, -1.8943923723335487, -2.2458461538461543, -2.494114796094994, -2.1132692307692307, -2.64, -5.47, -7.97, -11.52, -14.4, -17.3, -20.62, -20.63, -22.7,-25.2]
    frequenz_10k_100k = [math.log10(10000),math.log10(20000),math.log10(30000),math.log10(40000),math.log10(50000),math.log10(60000),math.log10(70000),math.log10(80000),math.log10(90000),math.log10(100000)]

    #plt.plot(frequenz_10k_100k, messdaten_14122022_10k_100k)
    #plt.xlabel('frequency')
    #plt.ylabel('phase')
    #plt.show()


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

    for i in range(0,len(signal1)):
        t.append(i)

    to = 10300


    plt.plot(t[10000:to], signal1[10000:to])
    plt.plot(t[10000:to], signal2[10000:to])
    #plt.show()

    t = []

    #cutoff: wird angegeben in vielfachen von der samplingfrequenz (10MHz).
    #hier: cutoff = freq*10 [TESTING]
    kern = signal.firwin(2047, cutoff = freq*10/10000000, window = "hamming")
    signal11 = signal.lfilter(kern, 1, signal1)[10000:]
    signal21 = signal.lfilter(kern, 1, signal2)[10000:]

    for i in range(0,len(signal11)):
        t.append(i)
    plt.plot(t[10000:to], signal11[10000:to])
    plt.plot(t[10000:to], signal21[10000:to])
    plt.show()

    t = []

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

    korr = []
    korr_steps = []
    temp_sum = []

    #Maxima der Verschiebungen
    neg_shift = -30
    pos_shift = 30

    do_analysis = True;

    if do_analysis == True:
        for j in range(0, int(len(signal1)/10000)-1):
            print(f"Fortschritt: {j*100/(int(len(signal1)/10000)-1)} %")
            for k in range(neg_shift, pos_shift):
                for i in range(10000*j, 10000*(j+1)-pos_shift):
                    if k < 0:
                        temp_sum.append(abs(signal1_shifted[i-k] - signal2_shifted[i]))
                    else:
                        temp_sum.append(abs(signal1_shifted[i] - signal2_shifted[i+k]))

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

        print(korr)
        print(f"average shift = {sum(korr_steps) / len(korr_steps)}")
        print(f"phase: {((sum(korr_steps)/len(korr_steps))/period)*360}")

        phases.append(((sum(korr_steps)/len(korr_steps))/period)*360)

    end = time.time()
    print("calc time: " + '{:5.3f}s'.format(end - start))


#print(korr)
#print(min(korr))
#for i in range(len(korr)):
#    if korr[i] == min(korr):
#        print("verschiebung: " + str(i))

    if do_analysis == False:

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

print(phases)


