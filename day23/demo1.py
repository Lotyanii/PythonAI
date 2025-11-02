import numpy as np
import torch

x = torch.tensor([[120, 220], [50, 80]])
x = x / 220
b = 1 / (1 + np.exp(-x))
print(b)
b = torch.sigmoid(x)
print(b)
s = torch.nn.Sigmoid()
b = s(x)
print(b)
