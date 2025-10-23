import torch

t1 = torch.tensor(1.0, dtype=torch.float32, requires_grad=True)
t2 = t1 + 1
t3 = 2 ** t2
t3.backward()
print(t3)
print(t1.grad)