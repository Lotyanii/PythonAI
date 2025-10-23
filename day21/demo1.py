import torch

t = torch.tensor([10, 20])
print(type(t))
print(t.shape)

npa = t.numpy()
t1 = torch.empty(size=(2, 3, 5))
print(t1)