import threading
from copy import deepcopy

import numpy as np


class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age


userList = [User('John', 36), User('Smith', 36)]
print(userList)

arr3d = np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
print(arr3d.shape)
# arr3d = arr3d.reshape(arr3d.size)
print(arr3d.shape)


copy = np.copy(arr3d)
print(arr3d.shape)

dp = deepcopy(arr3d)

print(id(copy))
print(id(dp))

print(np.sum(arr3d, axis=0))

def test():
    print(123)

threading.Thread(target=test).start()

