import math
import matplotlib.pyplot as plt
import numpy as np

print(math.log(0.5, 1-0.000011))
x = np.linspace(0,400000,100)
b_discharge = 1-0.000011
l_discharge = 1-0.00012
s_discharge = 1-0.021
battery = 458*0.97*0.97*pow(b_discharge,x)
cavern = 458*0.73*0.60
large = 458*pow(l_discharge, x)
small = 458*pow(s_discharge, x)

fig, ax = plt.subplots()
plt.plot(x, battery, 'g', label='battery')
plt.axhline(cavern, color='b', label='H2 cavern')
plt.plot(x, large, label='central heat storage')
plt.plot(x, small, label='small heat storage')

ax.set_ylabel('storage in GWh')
ax.set_xlabel('hours')
plt.legend()

plt.show()