import matplotlib.pyplot as plt
import random

x = [x for x in range(0, 101)]
y = [random.randint(0, 10) for _ in range(0, 101)]

plt.plot(x, y)
plt.savefig("test.png")
plt.show()

