import random

import torch


def loss_fn(output, target):
    loss = torch.mean(torch.square(output - target))
    return loss


def func1():
    # 训练数据
    x = torch.tensor((1, 2, 3, 4, 5, 6, 7, 8, 9, 10), dtype=torch.float32, requires_grad=False)
    y = 3 * x + 5 - random.uniform(-1, 1)

    # 模型
    w = torch.randn(1, dtype=torch.float32, requires_grad=True)
    b = torch.randn(1, dtype=torch.float32, requires_grad=True)

    # 定义学习率和迭代次数
    learning_rate = 0.01
    epochs = 1000

    # 存储损失值
    losses = []

    # 梯度下降
    for _ in range(epochs):
        # 前向传播
        y_pred = w * x + b

        # 计算损失（均方误差）
        loss = loss_fn(y_pred, y)

        # 反向传播
        loss.backward()

        print(w.grad)
        print(b.grad)
        print(loss)

        # 更新参数（梯度下降）
        with torch.no_grad():
            w -= learning_rate * w.grad
            b -= learning_rate * b.grad

            # 清零梯度
            w.grad.zero_()
            b.grad.zero_()

        losses.append(loss.item())



    print(f'\n最终参数: w = {w.item():.4f}, b = {b.item():.4f}')


if __name__ == '__main__':
    func1()
    pass
