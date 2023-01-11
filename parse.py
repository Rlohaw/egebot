import numpy as np
mass = [[i for i in range(0, 7)], [i for i in range(7, 14)]]
print(mass)
arr = np.array(mass)
arr = np.rot90(arr, k=-1)
print(arr)
