import torch


def pytorch_gradient_mechanism():
    print("\n=== PyTorch的梯度累积机制 ===\n")

    w = torch.tensor(3.0, requires_grad=True)

    print("PyTorch的梯度计算规则:")
    print("1. 每次调用 backward()，梯度会累加到 .grad 属性中")
    print("2. 不会自动清零")
    print("3. 需要手动调用 zero_grad()")

    print(f"\n演示:")
    print("初始: w.grad = {w.grad}")

    # 三次计算
    for i in range(3):
        y = w * (i + 1)
        loss = y ** 2
        loss.backward()
        print(f"第{i + 1}次backward后: w.grad = {w.grad.item()}")

    print("\n清零梯度:")
    w.grad.zero_()
    print(f"清零后: w.grad = {w.grad}")


pytorch_gradient_mechanism()