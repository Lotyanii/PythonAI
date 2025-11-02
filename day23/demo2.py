import torch
from torch import nn


# 全连接神经网络搭建
class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc_layers = nn.Sequential(
            nn.Linear(28 * 28, 512),
            nn.ReLU(),
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 10),
            nn.Softmax(dim=1)
        )

        pass

    def forward(self, x):
        out = self.fc_layers(x)
        return out
        pass

    pass


if __name__ == '__main__':
    input = torch.randn(1, 28 * 28)
    net = Net()
    val = net(input)
    print(val)
    print(val.size())

    pass
#
# # ont-hot 1 0 0 0 0 0 0 0 0 0
# x = torch.randn(1, 28 * 28)
# # 批次N V torch.randn(1, 28*28)
# # W * X
# # 参数在内部进行初始化 W, b
# m = nn.Linear(28 * 28, 10)
# output = m(x)
# softmax = torch.nn.Softmax(dim=1)
# output = softmax(output)
#
# print(output.size())
# print(output)
