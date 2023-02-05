import matplotlib.pyplot as plt
import math

messdaten_14122022_10k_100k = [-0.4496538461538462, -0.29423076923076924, -0.6916845530706917, -1.0163076923076924, -1.331826923076923, -1.610259488410749, -1.8943923723335487, -2.2458461538461543, -2.494114796094994, -2.1132692307692307, -2.64, -5.47, -7.97, -11.52, -14.4, -17.3, -20.62, -20.63, -22.7,-25.2]
frequenz_10k_100k = [math.log10(1000),math.log10(2000),math.log10(3000),math.log10(4000),math.log10(5000),math.log10(6000),math.log10(7000),math.log10(8000),math.log10(9000),math.log10(10000),math.log10(10000),math.log10(20000),math.log10(30000),math.log10(40000),math.log10(50000),math.log10(60000),math.log10(70000),math.log10(80000),math.log10(90000),math.log10(100000)]

plt.plot(frequenz_10k_100k, messdaten_14122022_10k_100k)
plt.xlabel('frequency')
plt.ylabel('phase')
plt.show()