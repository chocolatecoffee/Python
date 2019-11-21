import matplotlib.pyplot as plt
import numpy as np

names = ['s0', 's1', 's2', 's3', 's4', 's5']
values = [1, 10, 20, 30, 40, 100]

plt.figure(figsize=(9, 3))

plt.subplot(131)
plt.bar(names, values)
plt.subplot(132)
plt.scatter(names, values)
plt.subplot(133)
plt.plot(names, values)

plt.suptitle('Categorical Plotting')

plt.grid(True)
plt.show()
